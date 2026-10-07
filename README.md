# Filesystem Link Lifecycle Lab

An educational Python ledger showing how **names, file identities and open
references differ**. All inputs are invented declarations. The application does
not read target paths/identities/permissions, create links, open target files,
unlink names or measure storage.

The supported ordinary regular-file model requires retention while a declared
name or independent holding reference remains. Zero names **and** zero references
means modeled reclamation eligibility. Actual deletion, reclaimed bytes, secure
erasure, durability and permission authorization are always unverified.

## Run and demonstrate

Python3.13; standard library only, no package installation or API key. From this
directory:

```powershell
python -m lifecycle_lab demo
python -m lifecycle_lab --help
python -m unittest discover -s tests -v
python -O -m unittest discover -s tests -v
python tools/check_mutations.py
python tools/measure_report.py
```

The demo compares22 full reports against manually frozen expectations, including
invalid/unsupported controls. To send the two-file name-rebinding example through
bounded stdin:

```powershell
python -c "import json,sys; from lifecycle_lab.fixtures import oracles; sys.stdout.write(json.dumps(oracles()[9]['request']))" | python -m lifecycle_lab analyze
```

That trace starts with A→F and B→G. Opening A creates R→F; unlinking A retains R→F;
linking B to the now-free A produces A→G while R still refers to F. Closing R makes
F eligible in this ledger; G remains named. The model does not perform any event.

| Event | Ledger meaning |
| --- | --- |
| link | Add a new name for the existing source's file identity |
| unlink | Remove only one name; existing references remain bound |
| open | Create a fresh independent reference to the name's current file |
| close | Release only the named owned reference |

Exit0 complete trace/passing demo;1 failed demo;2 rejected/unsupported/over-limit or
invalid arguments;3 checked I/O failure. Eligibility is not a permission denial.
Reports are escaped compact UTF8 JSON+LF. Help is fixed text; parser errors are
fixed JSON without argv reflection. Text diagnostics use native newline. Writes
require exact builtin integer counts and flush; failure can leave partial output.

## Architecture and interface

`lifecycle_lab/core.py` validates exact builtin records before replaying the pure
ledger and creating detached snapshots. `evaluate(object)` and `analyze_json(bytes)`
are the public intake functions; `serialize_report(dict)` is a trusted internal
formatter, not arbitrary-object intake. `__main__.py` supplies bounded stdin and
checked demo/report/help/error delivery. `fixtures.py` copies trusted frozen data.

`fixtures/oracles.json` contains22 full independent reports. `fixtures/domain.json`
contains32 remaining-label permutation traces and150 initial/post-event snapshots.
Their pre-code hashes and the fixed contract are in `research/oracle-freeze.json`.
No expected data came from the application evaluator. See [PLAN.md](PLAN.md) and
[CONTRACT.md](CONTRACT.md) for exact shapes, ordering, statuses and error precedence.

Whole common validation precedes exclusions and replay. Invalid traces return no
initial/steps/final state, even after a valid local prefix. File/reference IDs are
not reused; name labels can rebind. Different domains may share labels or input
containers; every occurrence validates. Caller data stays unchanged and snapshots
cannot retroactively alter one another. Stable caller input during a call is required.

Limits:4 files,8 distinct names,8 historical reference IDs,24 events; raw32768 bytes,
container nesting6 (root1, scalar leaves add0), numeric token10 chars, ASCII IDs24,
keys/enums32, features16, output262144 bytes. Floats/nonfinite/duplicate-key JSON and
subclasses/bool-as-integer are rejected. Accepted max-cardinality stress produces
46,792 report bytes against a163,840 conservative bound. This is a measured admitted
stress case, not proof of a globally optimal maximum or hard resource containment.
Artificial output-cap/tiny-budget/deep invalid-parser seams are labeled separately.

## Security and limitations

Reference tokens are independently holding abstractions, **not file descriptors or
open-file-description identities**. Dup/fork/mmap/in-flight I/O, external refs,
descriptor reuse, tmpfile/link-from-reference, remote filesystems, crash/snapshot,
permissions/symlinks/races and richer contexts are unsupported. Rename/replacement
needs a different contract and is deferred. Events and complete reference coverage
are assumed, never authenticated or observed. No general filesystem/path/OS emulator.

An eligible catalog row is an explanation, not proof that an actual object exists
or its bytes were erased, reclaimable, recoverable, durable or authorized to delete.
See [SECURITY.md](SECURITY.md). Use invented public fixtures only; no real target
filesystem operations or third-party tests were performed.

## Verified results and learning

CPython3.13.7 Windows:31 tests normal and optimized,0failures/errors;70 real-child
observations per suite;22 full reports;32 finite traces/150 snapshots; four mutants
each one assertion/zero errors and all restored passes in both modes; both demos,
stress measurements, compile and application/tools Bandit pass. Final capture
explicitly confirms the test runner's stdout/stderr restoration. The first capture
lost its receipt due to a test-harness restoration bug; preserved and corrected.
Exact raw artifacts/check scope in [VERIFICATION.md](VERIFICATION.md).

ECC is an implementing-agent self-review, not independent audit or full native
plugin execution. No Linux/upstream/hosted CI/CodeQL/dedicated secret/history scan,
hard RSS/time measurement or real filesystem guarantee. No new repository, installs
or publication. Prior accepted labs remain separate and unchanged.

Optional exercise: in the rebinding trace, explain why closing R changes F's modeled
eligibility while A still names G. Then compare the two-open case where closing
one reference leaves another holding. [LEARNING.md](LEARNING.md) records lessons.

## Attribution and license

Original application/fixtures/tools: MIT, copyright2026 Jake France. Codex designed,
implemented, reviewed and tested with approved scope. One bounded local qwen3.5:2b
test-idea draft was rejected as an oracle; raw preserved, no remote/paid fallback.
Reviewed owned sticky-lab JSON/checked CLI/child harness patterns were adapted locally;
there are no sibling runtime imports. Research snapshots are separately labeled
public Apache2 pyfakefs/GPL2-or-later LTP source excerpts/docs, not original MIT code
or executed dependencies. [RESEARCH.md](RESEARCH.md) records exact blobs, source/
license/maintenance/CI/dependency comparison and retrieval gaps. Upstream copyright/
license notices stay with that upstream evidence. No upstream executable adoption.

## Publication status

See [publication review](PUBLICATION.md) for the October 5 source snapshot, fresh local checks, evidence boundaries and current hosted-check distinction.
