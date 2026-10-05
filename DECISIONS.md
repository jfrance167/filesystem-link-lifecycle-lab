# Decisions

- Original finite ledger rather than pyfakefs/LTP adoption: enough for the declared
  name/file/open-reference learning gap without monkeypatching/path/host operations.
- File catalog fixed, file/reference IDs not reused; name labels may rebind after
  unlink. Existing references retain original file binding. No creation/resurrection.
- Abstract independently holding tokens, not FDs/OFDs; dup/fork/mmap/async/external
  references explicit unsupported. Declared complete coverage/success unverified.
- Eligibility = zero names AND zero refs; no bytes, deletion/erasure/durability or
  permission outcome inferred. Retain catalog rows for explanation only.
- Full common validation before exclusions/replay; invalid trace discards prefix.
  Freeze full reports before core; detached snapshots and four logical mutants.
- Standard library with reviewed owned CLI/JSON patterns; no sibling runtime imports.
  Local draft not oracle; remote free guardrails unverified; Codex security judgment.
- Coordinator05:37 approved stages1-3; contract/full22 reports and32trace150prefix
  oracle/hash frozen before code. No new Git/CI/install/target/external permissions.
- Restore both public test streams after I/O seams; failed capture exposed a stderr-
  only patch that leaked detached stdout. Preserve failure, assert restoration and
  re-run actual final captures. This is harness correctness, not an independent audit.
- Measured admitted max-cardinality request/report4082/46792 bytes; conservative
  bound163840 still independent of reduced-cap seams. Do not claim global optimum.
