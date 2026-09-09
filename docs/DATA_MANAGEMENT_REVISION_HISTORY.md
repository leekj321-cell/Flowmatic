# Data Management — Revision / Reference / Offset History

Status: functional engine baseline, 2026-09-10

## Product contract

Data Management is the shared module that keeps manufacturing reference data and change history canonical across Machining, Quality, Operations, and Logistics.

It now has two explicit layers:

1. **Reference Master**
   - machine / product / process / tool / feature identity
   - approved baseline data
   - current NC revision and parent relationship
   - source, hash, manifest and approval state

2. **Change History**
   - NC revision chain
   - measurement-linked offset events
   - before / after values and timestamps
   - CSV export for Excel-style matrix review
   - integrity checks and stale-parent conflict gates

## Machining Intelligence loop

`Measure → Calculate correction → Generate new NC revision → Verify → Deploy → Record offset event → Update manifest`

G-code stays an execution artifact. A correction generates a new NC revision instead of appending a long history inside the program.

The canonical history is stored in SQLite and can be exported to CSV. The NC comment carries only compact identity such as:

```text
(FLOWMATIC REV=R020 HASH=4f20aa38c6d1)
```

## Offset matrix

Long-form history is stored per event:

`timestamp / machine / part / operation / NC revision / offset / before / after / measurement / target / source`

The Data Management module can export the same history as a matrix:

| Offset | 09/10 08:00 | 09/10 11:20 | 09/11 08:12 |
| --- | ---: | ---: | ---: |
| X20 | +67 | +69 | +72 |
| Y20 | +78.73 | +78.73 | +78.73 |
| Z20 | +89.98 | +89.98 | +90.11 |

Unchanged values may be carried forward for human review while the event ledger remains sparse.

## Offline / USB rule

Offline copies do not choose the latest file by Windows modified time. Canonical purity is checked by:

`asset key + revision id + parent revision + SHA-256`

If a local PC or USB package attempts to create a revision from a parent that is no longer canonical, the engine fails closed and sends the change to conflict review instead of overwriting the current baseline.

This engine is the persistence boundary for the planned Offline Relay. Network transport, CNC adapter writes, automatic machine execution, and physical acceptance remain separate deployment gates.

## Safety boundary

Measurement-linked correction and NC generation may be automated, but direct CNC execution is not implied by this module. Machine command transfer, controller-specific limits, simulation, approval, and rollback remain explicit gates.
