# Local verification - October5,2026

CPython3.13.7 Windows AMD64; final capture09:58:02 UTC. Existing Bandit1.9.4;
standard-library application, no installs. research/check-status.json records ten
checks, all exit0, with raw stdout/stderr preserved. Earlier successful mutation/
measurement/scanner receipts reused because their source stayed unchanged.

| Phase/check | Status and actual result |
| --- | --- |
| Tests normal | PASS31 tests,0failures/errors; public streams restored |
| Tests optimized | PASS31 tests,0failures/errors; public streams restored |
| Independent expected reports | PASS22 full reports, unchanged pre-code hashes |
| Finite remaining-label oracle | PASS32 traces,150 initial/post-event snapshots |
| Real CLI processes | PASS70 observations each suite, normal/-O children |
| Four mutants normal/-O | PASS each1assertion/0errors; restored four tests pass |
| Demos normal/-O | PASS22/22 expected reports; exit0 |
| Admitted stress normal/-O | PASS4,082 input/46,792 report bytes,24 events |
| Compile | PASS owned application/tests/tools |
| Bandit app/tools | PASS0findings/errors/skips/suppressions,1585 non-comment LoC incl trusted fixture data |
| ECC source/caller/test self-review | PASS after harness restoration fix/recheck; not independent |
| Types/lint | NOT RUN no configured tools; no install |
| Linux/upstream/hosted/CodeQL/independent/dedicated secret scanner | NOT RUN |
| Git diff/history | NOT APPLICABLE no repository initialization authorized |

Reproduce from the directory:

```text
python -m unittest discover -s tests -v
python -O -m unittest discover -s tests -v
python tools/check_mutations.py
python -O tools/check_mutations.py
python tools/measure_report.py
python -O tools/measure_report.py
python -m lifecycle_lab demo
python -O -m lifecycle_lab demo
python -m compileall -q lifecycle_lab tests tools
python -m bandit -r lifecycle_lab tools -f json
```

normal-suite.stdout.json / optimized-suite.stdout.json contain full logs and every
child's actual return/stdout/stderr/setup.70=22 native/healthy controls+48 labeled
seams (12short/flush,24float/bool/None/integer-subclass counts,12closed-Python/absent
streams). Both normal/optimized interpreters run in each parent suite. Barriers close
readers before output; ten-second child timeout is harness bound, not containment.
Binary LF reports versus native-newline diagnostics checked; healthy complete,
invalid-trace/incomplete/demo/help/parser controls. No actual target file operation.

mutations.stdout.txt and mutations-optimized.stdout.txt preserve assertion failures
and restorations. Ignored refs, unlink-all-names, close-all-refs and reference-retarget
faults are in-memory patches with one focused assertion each,0errors. No source
mutations or broad score. No-hook subclasses/metaclass/custom keys, aliases/repeated
occurrences/cycles/common-before-exclusion/replay/preconditions/immutable snapshots
and strict JSON/output seams covered. All frozen22 reports are full comparisons.

measure-report receipts include full admitted request/report. Four files, eight
initial names/references,24events and24-character IDs; repeated unlink/relink sustains
wide snapshots. Report46,792<163,840 conservative width envelope<262,144 cap; not
global optimum proof. Frame budget26×6144+4096=163840, ASCII fixed widths/≤4file rows/
≤16mappings; output/depth reduced/invalid-schema guards honestly labeled seams.
Demo actual bytes are recorded in source receipt. Accepted natural report overflow
is not claimed. Logical limits are not hard RSS/time guarantees.

First final-capture attempt FAILED in verifier JSON decode: text-count diagnostic
test patched stderr alone although main detaches BOTH public sinks; suite stdout
became None and JSON receipt wasn't delivered. Original empty stdout/stderr retained
as pre-restoration artifacts; cause/correction in capture-restoration-failure.json.
Fixed test to patch/restore both and assert identities. Final full suites verify
streams_restored=true; no original failed capture erased or counted as PASS.

Bandit scans lifecycle_lab/tools, not tests. Trusted child launches/fixture reads
manually reviewed. Core forbidden-call probes include builtins.open/exec/eval,
os.open/stat/link/unlink/rename/mode/system and socket/process calls after imports.
Source/content and bounded credential-pattern search found no private material/
matching keys; not a dedicated secret-scan safety verdict. No repository history.

Frozen CONTRACT/oracle/domain hashes in oracle-freeze.json predate application code.
Current source/tests/tools/raw/doc hashes and verified vault note are bound by
research/source-receipt.json. Integrity evidence, not a signature/authenticity/safety
proof. Earlier research-checkpoint is historical documentation-only evidence.
