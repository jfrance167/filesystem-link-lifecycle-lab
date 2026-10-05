# Link lifecycle research — October5,2026

Historical research phase coordinator05:12 under Jake's verified direct delegation,
before application code. Coordinator05:37 approved stages1-3, addendum frozen before
core. Current local completion in STATE/VERIFICATION; source observations/gaps below
remain research evidence, not upstream execution or independent audit.

## Reuse and learning gap

Read selected-vault Home/CodexIntegration, Linux File Modes and Directory Access,
File System Forensics Listing and Recovery Limits and accepted Sticky Directory
project note. Filename/topic search found related notes, not a standalone link
lifecycle lab; bounded search, not exhaustive. Sticky README/PLAN explicitly mark
actual entry removal/reclamation unverified. File-integrity-monitor README/code
references distinguish real path/content/metadata monitoring and real-file demos;
do not run/reuse those experiments. Prior strict JSON, exact identity admission,
immutable reports and corrected checked CLI/process harness are useful owned
patterns, not lifetime semantics. Existing parent has unrelated changes/untracked
projects; inspected status, preserved all. No prior suites rerun or source edited.

## Primary behavior and narrowing

[unlink(2)](https://man7.org/linux/man-pages/man2/unlink.2.html): name removal is
separate from file lifetime; remaining names or open references affect retention.
[link(2)](https://man7.org/linux/man-pages/man2/link.2.html): another name shares
file identity, rather than copying content; occupied destination is not overwritten.
[open(2)](https://man7.org/linux/man-pages/man2/open.2.html): descriptor refers to
an open-file description that survives name removal/rebinding. File ID/reference
binding must remain stable across a later reuse of the same synthetic name.
[close(2)](https://man7.org/linux/man-pages/man2/close.2.html): releasing the last
reference matters, but close is not a durability guarantee; in-flight operations and
error semantics complicate real reference lifetime. Therefore assume successful
events and exclude asynchronous activity/external refs; no failed-close prediction.
[dup(2)](https://man7.org/linux/man-pages/man2/dup.2.html): duplicates share open-file
description identity; proposed independent abstract holding tokens are not FDs/OFDs.
Dup/fork/mappings and descriptor reuse excluded, not silently simplified.
[rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html): source/destination,
replacement victim, same-file no-op and atomicity add cases; defer this alternative.

POSIX2024 unlink page attempted twice and returned internal access errors. No claim
that direct POSIX text was inspected; Linux primary pages establish the selected
ordinary subset. Neither those pages nor this ledger proves erase/recovery or actual
reclaimed storage. The retention/eligibility formula is a stated model inference
from declared complete names and independent references, not a real kernel audit.

## Connected GitHub candidate: pyfakefs

[pytest-dev/pyfakefs](https://github.com/pytest-dev/pyfakefs) is a credible filesystem
testing candidate; actual source/tests/docs/packaging/license/CI/issues inspected.
Repository API reports unarchived/public, pushed2026-09-28. Main commit metadata
returned796c48eb7830e3ee7fb57eb368dc115c1f3436ba,2026-09-22, root-rename permission
fix. Pushed date need not equal main commit date. Commit identity does not prove
safety. Search result stars were not used as quality evidence.

Actual source at that ref, with main/ref blob equality verified:

- pyfakefs/fake_filesystem.py blob6110aa5d2b3151170bc75214e8d987b731cc11d1:
  create_link resolves source/destination, checks existence/type/device and adds the
  same FakeFile; remove_object resolves path then removes one directory entry;
  close_open_file changes descriptor ownership bookkeeping. Broader path semantics.
- pyfakefs/fake_file.py blob4e30676b0f620d596f7d7455b61ce4d69966e546:
  add/remove entry adjusts st_nlink; remove_entry has Windows open-file rejection
  versus POSIX directory checks. It adjusts simulated disk usage at last directory
  link without an open-reference guard in that inspected branch. This is simulated
  accounting, not a physical-storage oracle. File-wrapper close_fd handles flush,
  ownership and delete-on-close; not a minimal independent token ledger.
- pyfakefs/tests/fake_filesystem_test.py blob4e0e63ec2e8f44a6032cc53714a879fcd66b5f81:
  hard-link used-size test holds usage through one unlink, then clears after the
  second. Shared-identity/nlink test and actual source corroborate link modeling.
- pyfakefs/tests/fake_os_test.py blob173dc46fb499be280b5b908b8acc1207874b3f7c:
  Windows/POSIX open-file removal controls and same-file rename no-op tests. Inspected
  controls show path existence, not full last-open-reference reclamation verification.
  Parts of the broader test suite deliberately use real filesystem access; no run.

README.md blob23ec944d08a8e90fb76602637bdeec1b098cc5dd describes monkeypatching,
real-source mapping/pause/unpatch and C-extension limitations. fake_open.py main
blobf7903b4dbae835a04f3763af5a230b5be6a40e31 has explicit excluded/unfaked path
fallback to io_open. It was read as research only, not main/ref-bound like core
files. Consequently pyfakefs is not a security isolation boundary for unfamiliar
code. This is documented capability/limitation, not a new vulnerability allegation.

pyproject.toml blob7fe1221dbdf849466f8b6251a5005b447b1e0cbf, main/ref equality:
Python≥3.10; no runtime dependencies declared in project field; build setuptools≥77;
dev pytest/pre-commit and optional extra/docs packages. tox includes supported
Python versions and all_tests/pytest integration. Classifier stability is upstream
self-description, not confirmation. No package/wheel/advisory/hash/install assessment
needed for chosen original stdlib approach; no third-party dependency proposed.

COPYING blob67db8588217f266eb561f75fae738656325deac9, main/ref equality: Apache2.0.
Adoption/derived redistribution requires license retention/change notices and any
applicable upstream attribution/NOTICE obligations; not adopting application code.
Research source text keeps headers and separate license evidence. Original future
implementation proposed MIT with source links/AI assistance/owned-pattern attribution.
No blanket license claim over upstream snapshots. CHANGES.md main
blobc40e74046b54570ef00784bb20bc64ac6864d0f0 lists release6.2.0,2026-04-12 and
current unreleased fixes, including cross-device hard-link and root rename fixes.

Actual `.github/workflows/testsuite.yml` pinned blobffbfef78c3690f6779edbd845c213fecc91c7f6d:
Linux/macOS/Windows CPython/PyPy matrix, pytype, unittest/pytest and dependency checks.
It installs/upgrades dependencies, uses mutable Action version tags and intentionally
runs real-filesystem tests and root tests. Maintenance/test breadth evidence, not
passing-results or a CI template to reuse. No workflows run/root/sudo/install.
Earlier guessed test.yml/tests.yml returned404; web tree discovered testsuite.yml.
Guessed fake_file_wrapper.py404; actual close methods found in fake_file.py.

Actual [issue1337](https://github.com/pytest-dev/pyfakefs/issues/1337), createdSept8,
closedSept9,2026: reported6.2.0 cross-device links erroneously succeeding. Current
create_link inspected EXDEV guard and changelog fix, not a reproduced test/audit.
Do not call the issue a verified exploitable security finding. Commit root-rename
fix and relevant maintenance are concrete evidence beyond star count. No Scorecard,
comprehensive advisory search, latest packaged artifact or independent audit claim.

## Native candidate/reference: LTP

[linux-test-project/ltp](https://github.com/linux-test-project/ltp), reused prior
inspected pinned dca9f0d272b2923256852fc37abd222b533d91e0 source/CI/license assessment
from accepted sticky RESEARCH (read, not rerun). Fresh unlink05.c fetch same ref/blob
8de2d8bc2573ff1021d9d954e15b62901e71b82c: ordinary/FIFO successful unlink and name
existence check, needs real temp directory. GPL2-or-later SPDX/header. It does not
test the proposed full open-reference lifetime matrix. Guessed unlink01.c404;
directory API fetch transport failed, so no exhaustive unlink inventory claim.
Prior inspected COPYING/Makefile/native dependencies, distro/compiler CI and latest
Oct1 commit evidence stay source observations, not current native run/advisory proof.
No fork/adoption: it requires actual C/host operations excluded in this assignment.
Fresh LTP COPYING fetch also had a transport failure; prior license/header evidence
retained, no claim a fresh full license snapshot was obtained.

Initial commit/list/issues REST calls had transport errors; metadata succeeded;
later commits/main and specific files/issue obtained. Preserve retrieval gaps, no
client/provider retry loop. Source snapshot manifest binds selected inspected text
excerpts (core/tests) or full small docs/license files, explicitly labeled;
only selected function/test/doc bodies were inspected, not a complete upstream audit.
An attempted bulk shell save hit Windows command-length error206 before launch;
bounded patch-based excerpt saves used instead, with no executable source created.

## Worker choice and recommendation

Read existing STARTUP/status/routing guide and inspected helper. One public bounded
test-idea brief through existing loopback-only Ollama qwen3.5:2b,30s220token limit:
exit0/stop6.349s152output tokens, load5.127s. Raw separately retained. Draft proposed
individual actions but omitted multi-link/whole independent traces and blurred
file-label retention wording; rejected as oracle. No generated code executed.
Codex retains source/security judgment and contract design. OpenRouter explicitly
considered; startup snapshot is stale/degraded with unverified free/logging/guardrail
checks. Shared-write exclusion prevents refreshing it; no eligible verified-free
remote call. No retry/paid fallback/newspending. Laya schemas unrelated. Firecrawl
installed but zero-price eligibility unknown; included web/connected GitHub equivalent
used and failures disclosed. Local service readiness alone is not inference evidence;
this attempt's saved metadata is actual inference evidence.

Recommend BUILD original bounded stdlib ledger rather than adopt/fork. Research
justifies one precise supplied regular-file subset and preserves platform/context/
reference/actual-deletion limitations. PLAN defines schema/order/caps,22 independent
full-report design and32trace/150prefix finite domain, four mutations, threat model
and three stages subsequently approved/completed locally. No application code/tests
existed in the research-only phase; no target host experiments were performed.
