"""Flowmatic canonical revision and offset-history engine.

Design contract
---------------
- NC/G-code files are immutable execution artifacts. A correction produces a new revision.
- Full change history lives outside the NC file in SQLite and exportable CSV.
- The NC comment carries only compact revision identity, never the canonical history.
- Parent/hash validation prevents a stale offline PC or USB relay from silently
  overwriting the latest canonical revision.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping


class RevisionConflict(RuntimeError):
    """Raised when a new revision is based on a non-canonical parent."""


class IntegrityError(RuntimeError):
    """Raised when content does not match the canonical revision hash."""


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _num(value: Decimal | float | int | str | None) -> str | None:
    if value is None:
        return None
    return format(Decimal(str(value)), "f")


@dataclass(frozen=True)
class RevisionRecord:
    asset_key: str
    revision_id: str
    parent_revision_id: str | None
    content_sha256: str
    created_at: str
    source: str
    metadata_json: str


@dataclass(frozen=True)
class OffsetEvent:
    event_id: int
    timestamp: str
    machine_id: str
    part_id: str
    operation_id: str
    asset_key: str
    nc_revision: str
    offset_id: str
    before_value: str | None
    after_value: str
    measurement_value: str | None
    target_value: str | None
    source: str
    reason: str | None
    actor: str | None


class RevisionHistoryEngine:
    """Canonical ledger shared by Revision and Data Management modules."""

    SCHEMA_VERSION = 1

    def __init__(self, db_path: str | Path = ":memory:") -> None:
        self.db_path = str(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> "RevisionHistoryEngine":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def _init_schema(self) -> None:
        self.conn.executescript(
            """
            PRAGMA foreign_keys = ON;
            CREATE TABLE IF NOT EXISTS schema_meta (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS nc_revision (
                asset_key TEXT NOT NULL,
                revision_id TEXT NOT NULL,
                parent_revision_id TEXT,
                content_sha256 TEXT NOT NULL,
                created_at TEXT NOT NULL,
                source TEXT NOT NULL,
                metadata_json TEXT NOT NULL DEFAULT '{}',
                PRIMARY KEY (asset_key, revision_id)
            );
            CREATE INDEX IF NOT EXISTS idx_nc_revision_asset_time
                ON nc_revision(asset_key, created_at, revision_id);

            CREATE TABLE IF NOT EXISTS offset_event (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                machine_id TEXT NOT NULL,
                part_id TEXT NOT NULL,
                operation_id TEXT NOT NULL,
                asset_key TEXT NOT NULL,
                nc_revision TEXT NOT NULL,
                offset_id TEXT NOT NULL,
                before_value TEXT,
                after_value TEXT NOT NULL,
                measurement_value TEXT,
                target_value TEXT,
                source TEXT NOT NULL,
                reason TEXT,
                actor TEXT,
                FOREIGN KEY (asset_key, nc_revision)
                    REFERENCES nc_revision(asset_key, revision_id)
            );
            CREATE INDEX IF NOT EXISTS idx_offset_event_context_time
                ON offset_event(machine_id, part_id, operation_id, timestamp, event_id);
            """
        )
        self.conn.execute(
            "INSERT OR REPLACE INTO schema_meta(key, value) VALUES('schema_version', ?)",
            (str(self.SCHEMA_VERSION),),
        )
        self.conn.commit()

    @staticmethod
    def sha256(content: bytes | str) -> str:
        raw = content.encode("utf-8") if isinstance(content, str) else content
        return hashlib.sha256(raw).hexdigest()

    def latest_revision(self, asset_key: str) -> RevisionRecord | None:
        row = self.conn.execute(
            """
            SELECT * FROM nc_revision
            WHERE asset_key = ?
            ORDER BY created_at DESC, rowid DESC
            LIMIT 1
            """,
            (asset_key,),
        ).fetchone()
        return RevisionRecord(**dict(row)) if row else None

    def get_revision(self, asset_key: str, revision_id: str) -> RevisionRecord | None:
        row = self.conn.execute(
            "SELECT * FROM nc_revision WHERE asset_key = ? AND revision_id = ?",
            (asset_key, revision_id),
        ).fetchone()
        return RevisionRecord(**dict(row)) if row else None

    def register_nc_revision(
        self,
        *,
        asset_key: str,
        revision_id: str,
        content: bytes | str,
        parent_revision_id: str | None = None,
        created_at: str | None = None,
        source: str = "generator",
        metadata: Mapping[str, Any] | None = None,
        enforce_latest_parent: bool = True,
    ) -> RevisionRecord:
        if not asset_key.strip() or not revision_id.strip():
            raise ValueError("asset_key and revision_id are required")

        latest = self.latest_revision(asset_key)
        if enforce_latest_parent:
            if latest is None and parent_revision_id is not None:
                raise RevisionConflict(
                    f"{asset_key}: first revision cannot declare parent {parent_revision_id}"
                )
            if latest is not None and parent_revision_id != latest.revision_id:
                raise RevisionConflict(
                    f"{asset_key}: expected parent {latest.revision_id}, got {parent_revision_id}"
                )

        created = created_at or _now_iso()
        metadata_json = json.dumps(metadata or {}, ensure_ascii=False, sort_keys=True)
        record = RevisionRecord(
            asset_key=asset_key,
            revision_id=revision_id,
            parent_revision_id=parent_revision_id,
            content_sha256=self.sha256(content),
            created_at=created,
            source=source,
            metadata_json=metadata_json,
        )
        try:
            self.conn.execute(
                """
                INSERT INTO nc_revision(
                    asset_key, revision_id, parent_revision_id, content_sha256,
                    created_at, source, metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.asset_key,
                    record.revision_id,
                    record.parent_revision_id,
                    record.content_sha256,
                    record.created_at,
                    record.source,
                    record.metadata_json,
                ),
            )
        except sqlite3.IntegrityError as exc:
            raise RevisionConflict(
                f"{asset_key}: revision {revision_id} already exists"
            ) from exc
        self.conn.commit()
        return record

    def verify_revision_content(
        self, *, asset_key: str, revision_id: str, content: bytes | str
    ) -> bool:
        record = self.get_revision(asset_key, revision_id)
        if record is None:
            raise KeyError(f"unknown revision: {asset_key}/{revision_id}")
        return record.content_sha256 == self.sha256(content)

    def require_revision_content(
        self, *, asset_key: str, revision_id: str, content: bytes | str
    ) -> None:
        if not self.verify_revision_content(
            asset_key=asset_key, revision_id=revision_id, content=content
        ):
            raise IntegrityError(f"hash mismatch: {asset_key}/{revision_id}")

    def record_offset_event(
        self,
        *,
        timestamp: str | None,
        machine_id: str,
        part_id: str,
        operation_id: str,
        asset_key: str,
        nc_revision: str,
        offset_id: str,
        after_value: Decimal | float | int | str,
        before_value: Decimal | float | int | str | None = None,
        measurement_value: Decimal | float | int | str | None = None,
        target_value: Decimal | float | int | str | None = None,
        source: str = "manual",
        reason: str | None = None,
        actor: str | None = None,
    ) -> OffsetEvent:
        if self.get_revision(asset_key, nc_revision) is None:
            raise KeyError(f"unknown revision: {asset_key}/{nc_revision}")
        ts = timestamp or _now_iso()
        values = (
            ts,
            machine_id,
            part_id,
            operation_id,
            asset_key,
            nc_revision,
            offset_id,
            _num(before_value),
            _num(after_value),
            _num(measurement_value),
            _num(target_value),
            source,
            reason,
            actor,
        )
        cur = self.conn.execute(
            """
            INSERT INTO offset_event(
                timestamp, machine_id, part_id, operation_id, asset_key,
                nc_revision, offset_id, before_value, after_value,
                measurement_value, target_value, source, reason, actor
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            values,
        )
        self.conn.commit()
        return self.get_offset_event(int(cur.lastrowid))

    def get_offset_event(self, event_id: int) -> OffsetEvent:
        row = self.conn.execute(
            "SELECT * FROM offset_event WHERE event_id = ?", (event_id,)
        ).fetchone()
        if row is None:
            raise KeyError(f"unknown offset event: {event_id}")
        return OffsetEvent(**dict(row))

    def iter_offset_events(
        self,
        *,
        machine_id: str | None = None,
        part_id: str | None = None,
        operation_id: str | None = None,
        asset_key: str | None = None,
    ) -> list[OffsetEvent]:
        clauses: list[str] = []
        params: list[str] = []
        for column, value in (
            ("machine_id", machine_id),
            ("part_id", part_id),
            ("operation_id", operation_id),
            ("asset_key", asset_key),
        ):
            if value is not None:
                clauses.append(f"{column} = ?")
                params.append(value)
        where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        rows = self.conn.execute(
            f"SELECT * FROM offset_event{where} ORDER BY timestamp, event_id",
            params,
        ).fetchall()
        return [OffsetEvent(**dict(row)) for row in rows]

    def export_offset_history_csv(
        self,
        path: str | Path,
        *,
        machine_id: str | None = None,
        part_id: str | None = None,
        operation_id: str | None = None,
        asset_key: str | None = None,
    ) -> Path:
        events = self.iter_offset_events(
            machine_id=machine_id,
            part_id=part_id,
            operation_id=operation_id,
            asset_key=asset_key,
        )
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        fields = [
            "event_id", "timestamp", "machine_id", "part_id", "operation_id",
            "asset_key", "nc_revision", "offset_id", "before_value",
            "after_value", "measurement_value", "target_value", "source",
            "reason", "actor",
        ]
        with out.open("w", newline="", encoding="utf-8-sig") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields)
            writer.writeheader()
            for event in events:
                writer.writerow(asdict(event))
        return out

    def export_offset_matrix_csv(
        self,
        path: str | Path,
        *,
        machine_id: str,
        part_id: str,
        operation_id: str,
        carry_forward: bool = True,
    ) -> Path:
        events = self.iter_offset_events(
            machine_id=machine_id, part_id=part_id, operation_id=operation_id
        )
        timestamps = list(dict.fromkeys(event.timestamp for event in events))
        offsets = sorted({event.offset_id for event in events})
        direct = {(event.offset_id, event.timestamp): event.after_value for event in events}

        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", newline="", encoding="utf-8-sig") as fh:
            writer = csv.writer(fh)
            writer.writerow(["Offset", *timestamps])
            for offset_id in offsets:
                row = [offset_id]
                current = ""
                for ts in timestamps:
                    if (offset_id, ts) in direct:
                        current = direct[(offset_id, ts)]
                    row.append(current if carry_forward else direct.get((offset_id, ts), ""))
                writer.writerow(row)
        return out

    def revision_manifest(self, *, asset_key: str, revision_id: str) -> dict[str, Any]:
        revision = self.get_revision(asset_key, revision_id)
        if revision is None:
            raise KeyError(f"unknown revision: {asset_key}/{revision_id}")
        events = self.conn.execute(
            """
            SELECT event_id, timestamp, offset_id, before_value, after_value,
                   measurement_value, target_value, source, reason
            FROM offset_event
            WHERE asset_key = ? AND nc_revision = ?
            ORDER BY timestamp, event_id
            """,
            (asset_key, revision_id),
        ).fetchall()
        return {
            "schema_version": self.SCHEMA_VERSION,
            "asset_key": revision.asset_key,
            "revision_id": revision.revision_id,
            "parent_revision_id": revision.parent_revision_id,
            "content_sha256": revision.content_sha256,
            "created_at": revision.created_at,
            "source": revision.source,
            "metadata": json.loads(revision.metadata_json),
            "offset_events": [dict(row) for row in events],
        }

    def export_manifest_json(
        self, path: str | Path, *, asset_key: str, revision_id: str
    ) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            json.dumps(
                self.revision_manifest(asset_key=asset_key, revision_id=revision_id),
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        return out

    def nc_identity_comment(self, *, asset_key: str, revision_id: str) -> str:
        revision = self.get_revision(asset_key, revision_id)
        if revision is None:
            raise KeyError(f"unknown revision: {asset_key}/{revision_id}")
        return (
            f"(FLOWMATIC REV={revision.revision_id} "
            f"HASH={revision.content_sha256[:12]})"
        )
