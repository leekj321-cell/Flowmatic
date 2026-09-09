from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from flowmatic_core.revision_history import RevisionConflict, RevisionHistoryEngine


class RevisionHistoryEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "ledger.db"
        self.engine = RevisionHistoryEngine(self.db)
        self.asset = "MC01/PART123/OP20"

    def tearDown(self) -> None:
        self.engine.close()
        self.tmp.cleanup()

    def test_revision_chain_and_integrity(self) -> None:
        self.engine.register_nc_revision(asset_key=self.asset, revision_id="R001", content="G0 X0")
        self.engine.register_nc_revision(asset_key=self.asset, revision_id="R002", parent_revision_id="R001", content="G0 X1")
        self.assertTrue(self.engine.verify_revision_content(asset_key=self.asset, revision_id="R002", content="G0 X1"))
        self.assertEqual(self.engine.latest_revision(self.asset).revision_id, "R002")

    def test_stale_parent_is_fail_closed(self) -> None:
        self.engine.register_nc_revision(asset_key=self.asset, revision_id="R001", content="G0 X0")
        with self.assertRaises(RevisionConflict):
            self.engine.register_nc_revision(asset_key=self.asset, revision_id="R002", parent_revision_id="STALE", content="G0 X1")

    def test_offset_matrix_carries_latest_values(self) -> None:
        self.engine.register_nc_revision(asset_key=self.asset, revision_id="R001", content="G0 X0")
        self.engine.register_nc_revision(asset_key=self.asset, revision_id="R002", parent_revision_id="R001", content="G0 X1")
        t1 = "2026-09-10T08:00:00+09:00"
        t2 = "2026-09-10T11:20:00+09:00"
        for offset_id, value in (("X20", "67"), ("Y20", "78.73"), ("Z20", "89.98")):
            self.engine.record_offset_event(timestamp=t1, machine_id="MC01", part_id="PART123", operation_id="OP20", asset_key=self.asset, nc_revision="R001", offset_id=offset_id, after_value=value, source="measurement")
        self.engine.record_offset_event(timestamp=t2, machine_id="MC01", part_id="PART123", operation_id="OP20", asset_key=self.asset, nc_revision="R002", offset_id="X20", before_value="67", after_value="69", measurement_value="20.018", target_value="20.000", source="auto-compensation")

        output = self.engine.export_offset_matrix_csv(Path(self.tmp.name) / "offset_matrix.csv", machine_id="MC01", part_id="PART123", operation_id="OP20")
        with output.open("r", encoding="utf-8-sig", newline="") as fh:
            rows = list(csv.reader(fh))

        self.assertEqual(rows[0], ["Offset", t1, t2])
        self.assertEqual(rows[1], ["X20", "67", "69"])
        self.assertEqual(rows[2], ["Y20", "78.73", "78.73"])
        self.assertEqual(rows[3], ["Z20", "89.98", "89.98"])

    def test_nc_comment_is_identity_only(self) -> None:
        revision = self.engine.register_nc_revision(asset_key=self.asset, revision_id="R001", content="G0 X0")
        comment = self.engine.nc_identity_comment(asset_key=self.asset, revision_id="R001")
        self.assertIn("REV=R001", comment)
        self.assertIn(revision.content_sha256[:12], comment)
        self.assertNotIn("OFFSET", comment)


if __name__ == "__main__":
    unittest.main()
