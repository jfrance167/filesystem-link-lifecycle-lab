# Security model

Assets: host integrity, honest bounded reports, caller data and historical ledger
states. Untrusted declarations/raw JSON are data; fixed schema, source-backed model
and independently frozen fixtures are trusted code/design. Reports are advisory.
Formatter accepts trusted constructed reports, not arbitrary Python objects.

Threats/controls:

- Ambiguous/coercive/cyclic/oversized data: exact shapes/native-type identity before
  hooks, bounded keys/IDs/counts, strict capped JSON, duplicate-key/floating/nonfinite
  rejection; all occurrences/common fields before exclusion or replay. No global
  alias cache skips validation. Caller allocations and concurrent mutation excluded.
- False event/coverage declarations: explicit assumptions/unsupported richer
  contexts/unverified fields. Valid lies remain possible; no input authentication.
- Premature eligibility/ownership confusion: derived name/ref counts, stable file
  bindings, release one owned token/name, historical reference-ID reuse rejection;
 22 full independent reports/32 finite traces and four targeted assertion mutants.
- Snapshot aliasing/invalid prefixes: fresh detached snapshots; invalid replay
  returns no state or prefix. Pure local processing is not OS rollback/transaction.
- Resource/output control: raw32768/depth6/numeric10/list/ID limits and escaped
  output262144; conservative bound163840 with measured46,792-byte admitted stress.
  No hard memory/time isolation, globally maximal report or atomic delivery claim.
- Dirty/closed/short/noninteger output: exact integer write counts/flush, detach both
  public sinks on failure, fixed diagnostic and controlled exit3 in actual children.
  Partial bytes can be delivered; no rollback. Parser/help text does not echo argv.

Only supplied ordinary regular-file independent references modeled. Dup/fork/mmap/
async/external holders, descriptor reuse, tmpfile/linkat-reference, remote/snapshot/
crash/permissions/symlink/race/secure erase and rename/replacement unsupported.
No actual deletion/reclamation/erasure/durability/access/recovery verdict.

Core imports json/re only, without filesystem/network/process/identity capabilities.
Owned test harness reads its frozen artifacts and launches this trusted Python
module with invented data under bounded waits; no unfamiliar code or target operation.
Application source and ordinary verification artifacts are workflow files, not target
filesystem experiments. No host links/unlinks/open/stat/rename/chmod/chown/ACL tests.

No external reporting/integration configured. Review security concerns locally with
Jake. Local preparation does not authorize publication/merge/deployment or a new
repository. Linux/upstream/hosted/independent/security-certification limits retained.
