# Filesystem Link Lifecycle Lab - approved plan

Tier3 learning project; coordinator05:12 authorized research,05:37 approved stages1-3
under Jake's verified direct overnight mandate. Sole writer in this existing chat,
separate directory. CONTRACT records approval/addendum before core. No Git,
installs, host experiments or external actions. Stop new scope Oct6 08:00 Eastern.

## Objective, recommendation and alternatives

Explain supplied name → file identity and open reference → file identity separately.
Removing one name does not remove other names or retarget existing references.
In a declared ordinary regular-file trace, modeled retention is required while
at least one declared name or independent open reference remains. Zero of both
means **modeled reclamation eligibility**, never observed deletion, reclaimed bytes,
secure erasure, durability, permission authorization or file recoverability.

Recommend original standard-library `link_lifetime_v1`, a finite in-memory ledger
with link/unlink/open/close events assumed successful. Compare rename/replacement:
it adds two-name transitions, destination victims, same-file no-ops, exchange/flags
and atomicity/error semantics. Source and tests support those distinctions but that
extension adds unnecessary policy; defer it. General pyfakefs adoption/fork would
add platform/path/patching/real-source fallback and a much broader surface. LTP is
native live-operation testing, not a pure ledger. No suitable ready-to-adopt bounded
tool found in the performed reuse/candidate searches; not an exhaustive claim.

Success: independently frozen full reports, two-file name rebinding without reference
retargeting, last-name versus last-reference cases, all-common validation before
exclusions/replay, exact owned-reference closure, bounded snapshots and truthful
statuses. Use only invented ASCII labels, not paths/descriptors/inode numbers.

## Exact proposed input and admission

Root exact dict keys: id,version,profile,files,names,references,events,context.
Every record/container type admitted by identity before length/iteration/equality/
hashing; native keys exact str, length≤32 before set comparison. IDs exact ASCII
str `[A-Za-z][A-Za-z0-9_-]{0,23}` (1..24). Keys are fixed. No coercion or subclasses,
including metaclass equality/hash. Numeric version exact int0..999999999; bool invalid.
Version1 and profile `link_lifetime_v1` supported; other bounded well-formed version/
profile unsupported. Profile follows ID grammar. No paths, bytes content or user code.

- files: exact list1..4 of exact {id,kind}. Unique file IDs; kind exact enum regular,
  directory,symlink,other,unknown. Only regular supported. File catalog is fixed for
  a trace, never reused, created or resurrected by an event.
- names: exact list0..8 of exact {id,file_id}. Unique live name labels; each points
  to a catalog file. Name labels are case-sensitive and can be reused after unlink;
  this models a name being rebound, not file identity reuse.
- references: exact list0..8 of exact {id,file_id}. Unique independent holding open
  reference IDs; each points to a catalog file. These are abstract reference tokens,
  **not descriptors or open-file-description identities**. Initial refs may retain a
  nameless file. Each initial file needs ≥1 name/reference; an initially unrepresented
  file is rejected, not assumed reclaimed. No historical ref-ID reuse in this lab.
- events: exact list0..24; unique event IDs. Each exact record has id,op and the
  fields below. All fields validate even for unsupported operations or later events.
- context: exact {platform,reference_coverage,event_outcomes,excluded_features}.
  platform posix_regular/windows/unknown; coverage complete_declared/partial/unknown;
  outcomes assumed_success/failed/unknown. Only first of each supported. All are
  declarations, not verified observations. excluded_features exact list0..16,
  unique exact strings from dup,fork,mmap,async_io,tmpfile,remote_fs,snapshot,crash,
  permissions,symlink,race,external_refs,secure_erase,descriptor_reuse. Any listed
  feature unsupported. Unknown enum strings rejected. Enum length≤32 before lookup.

Event shapes (all values exact IDs):

| op | Additional keys | Supported effect/preconditions |
| --- | --- | --- |
| link | source_name,new_name | Source live; destination absent. Add same file identity. |
| unlink | name | Name live. Remove only this label. References unaffected. |
| open | name,reference_id | Name live; reference ID never used before. Bind to current file. |
| close | reference_id | Reference live. Remove only this owned token. Names unaffected. |
| rename,replace | source_name,new_name | Known unsupported; both fields still validate. |
| link_from_reference | reference_id,new_name | Known unsupported; no linkat/ref resurrection. |

Across initial/event labels, at most8 distinct name IDs and8 distinct reference IDs
per trace. Count each occurrence before dedup; enforce raw list caps first. Historical
reference tokens count against this bound, even after closing. Different kind/record
shapes prevent valid container alias shortcuts; validate each occurrence without a
global visited cache. Repeated immutable leaves validate repeatedly; cycles fail
shape/scalar admission without arbitrary recursive walking. Caller input stays
unchanged; stable input during evaluation required, no concurrent mutation support.

Raw JSON exact bytes≤32768 before decode; strict UTF8; structural depth≤6 outside
quoted strings; numeric token≤10 chars; no duplicate keys, floats or nonfinite values.
Proposed validation order: raw limits/decode/parser → root shape → id/version/profile
→ files fields/count → names fields/count → references fields/count → ALL events
fields/count → context fields/features → identity uniqueness/initial relationships/
distinct-label caps → collect sorted known exclusions → replay. First common failure
wins. Malformed late event or initial relationship beats early exclusion/replay error.
Unsupported kinds/version/profile/context/known ops never yield partial decisions.

Replay consumes no ambient state. On first invalid transition, reject entire report
with fixed violation + zero-based event_index, no initial/steps/final/prefix outcome.
Violations: missing_name,name_exists,missing_reference,reference_reuse. For link,
source missing precedes destination occupied; for open, name missing precedes
reference reuse. No failed operation prediction/errno emulation; these are violations
of an assumed-success trace. An earlier valid prefix does not authorize its effects.

## Output/status and bounds

All reports: status,complete,reason; actual_deletion/storage_reclaimed/secure_erasure/
durability/permission_authorization all `unverified`; assumptions ordered
[invented_ids,declared_complete_references,events_assumed_successful,ordinary_regular_subset];
not_verified ordered [input_truth,reference_coverage,actual_deletion,storage_reclaimed,
secure_erasure,durability,permission_authorization].

Complete: status=model_complete,complete=true,reason=declared_lifetime_trace_only,
plus id,profile,initial,steps,final. Each snapshot exact {names,references,files}.
Names/references sorted by id, exact {id,file_id}. Files sorted by id, exact
{id,link_count,open_reference_count,retention_basis,reclamation_eligible}.
Counts derived from current mappings, not trusted caller counters. Basis:
names_and_references/names_only/references_only/none; eligibility true iff counts
both zero. Catalog rows remain in all snapshots even when eligible; no claim an
actual kernel object still exists. Steps contain index,id,op,state; state is after
that event. Initial is before events; final equals last state or initial for no events.
Snapshots detached, no mutable-state aliases that retroactively change earlier steps.

Unsupported: complete=false,reason=outside_subset, sorted unsupported_reasons for
version/profile/kind_ID/context_FIELD_VALUE/feature_LABEL/op_EVENTID_LABEL. No state.
Rejected fixed reasons: object_shape,identifier,integer_range,enum,list_shape,
duplicate_identity,unknown_file,initial_unreferenced_file,duplicate_feature,
invalid_transition (with fixed violation/index),input_type,duplicate_key,
non_integer_number,invalid_json_or_utf8. Over-limit fixed reasons: input_limit,
depth_limit,numeric_token_limit,list_limit,identifier_count_limit,output_limit.
Unknown caller values never reflected in errors. Only exact bounded admitted IDs
are present in successful reports and known unsupported-reason labels.

Trusted internal report serializer: escaped compact JSON+LF≤262144 bytes. Conservative
proposed width budget: ≤26 snapshot frames (initial+24steps+final), each ≤6144 bytes
(four file rows≤512 each,16 mappings≤128 each,2048 frame/step allowance), plus4096
metadata =163840<262144. Establish exact serialized max-shape measurement and verify
this bound before completion, not claim a measured bound now. Demo contains only
fixed small fixtures; measure its actual report separately. Oversize trusted formatter
guard returns incomplete output_limit, no state, no recursive fallback; tiny-budget
guard raises controlled internal error. Label artificial/reduced-cap seams; no hard
RSS/time isolation or atomic output promise.

CLI proposed `python -m lifecycle_lab analyze|demo|--help`; bounded stdin cap+1, no
files/network/host operations. Exit0 complete model or passing demo (eligibility is
not a denial/permission verdict);1 failed demo;2 rejected/unsupported/over-limit or
invalid arguments;3 I/O failure. Fixed trusted help. Fixed parser JSON no argv
reflection. Binary report LF; text diagnostic native newline. Every write return
must be exact builtin int equal to length; check flush. On failures detach both
dirty public sinks before checked fixed diagnostic; closed-Python ValueError and
absent sinks controlled. Native and synthetic child shutdown normal/-O required.

## Independent pre-code oracle design

After scope approval, manually freeze FULL requests/reports and schema/error/bounds
receipt before application code. Table below is a proposed independent reference
design, not application-generated truth. Defaults F←A, no refs; other labels unique.
Each frozen report includes every snapshot/mapping/count/basis/eligibility/metadata.

| Case | Invented trace / variation | Independent expected endpoint |
| --- | --- | --- |
| 01 | No events | F one name,0refs,names_only,false |
| 02 | link A→B | F two names,0refs,false |
| 03 | link A→B; unlink A | Only B→F survives,false |
| 04 | link A→B; unlink A; unlink B | F zero/zero,none,true |
| 05 | open A→R; unlink A | R→F persists,zero/one,references_only,false |
| 06 | open A→R; unlink A; close R | zero/zero,true |
| 07 | open A→R; close R | A→F remains,one/zero,false |
| 08 | open A→R; open A→S; unlink A; close R | S→F only,zero/one,false |
| 09 | Case08 then close S | zero/zero,true |
| 10 | F←A,G←B; open A→R; unlink A; link B→A; close R | R bound F before close; F eligible; A/B→G,G two names |
| 11 | Initial F nameless,R→F; close R | F eligible; valid initial holding ref |
| 12 | Initial F←A,R→F; close R | F still named,false |
| 13 | unlink Missing | invalid_transition/missing_name,index0,no prefix |
| 14 | link A→A | name_exists,index0,no prefix |
| 15 | open A→R; close R; close R | missing_reference,index2,no prefix |
| 16 | open A→R; close R; open A→R | reference_reuse,index2,no prefix |
| 17 | link Missing→B | missing_name,index0,no prefix |
| 18 | known rename with malformed later field | common rejection before exclusion |
| 19 | well-formed rename A→B | unsupported,no states |
| 20 | partial coverage plus unlink Missing | unsupported before replay,no states |
| 21 | Initial name points to absent file ID | rejected/unknown_file,no states |
| 22 | Catalog file has no initial name/ref | rejected/initial_unreferenced_file |

Independent finite domain: initial F with names A/B and0,1,2 distinct initial refs;
all permutations of removing both names and closing all refs:2!+3!+4!=32 traces,
150 prefix snapshots (2×3+6×4+24×5). Expected counts/bases from remaining-label sets,
without production transition functions. Frozen before code; only finite-domain
coverage, not OS coverage. Fixed cases cover additions/name rebind/multiple files.
Metamorphic input-order invariance (for initial catalogs), input preservation,
snapshot independence, unrelated-file isolation; no silently reordered events.

Four assertion mutants: eligibility ignores refs; unlink removes all names of file;
close removes all refs to file; rebind retargets an existing reference. Each must
cause an assertion, not only an error; preserve raw failure/restoration evidence.
All common/unknown/limit precedence, late invalid behind early bad transition/
unsupported, exact-type/metaclass/custom-key/cycle/repeated-alias probes required.

## Architecture, threat model and stages

Stdlib only: pure lifecycle_lab/core.py (admission, ledger, snapshots, JSON),
__main__.py checked delivery, detached trusted fixtures.py; frozen fixtures/oracles.json;
tests core/CLI/actual-process, owned tools/check_mutations.py. Reuse reviewed strict
JSON and corrected delivery patterns from prior owned lab only after approval;
no sibling runtime imports, upstream dependencies or executable candidate adoption.
Original idiomatic functions, docs for public API, comments for security reasoning.

Assets: host integrity, honest reports, unchanged caller data and historical state.
Threats: coercive/ambiguous/cyclic/oversized input; false coverage/success declarations;
premature eligibility, identity/ref ownership confusion, snapshot aliasing, output
failure/reflection and treating eligibility as real deletion/secure erasure.
Controls: exact bounded schema/whole-input validation, fixed IDs/counters derived
from mappings, owned token removal, detached snapshots, independent oracles/mutants,
checked escaped output and explicit unverified claims. Stable input assumed. No
control authenticates events/coverage or establishes real filesystem guarantees.

1. Contract/oracles and pure ledger. Approval required first. Freeze22 full reports,
   schema/status/precedence/domain/hash before core. Verify source-backed transitions,
   all-field/no-hook/alias/immutability tests and independent32trace/150prefix domain.
2. Strict JSON/CLI/demo. Depends1; verify bounds/admitted max report width, duplicates/
   floats/UTF8/cap seams, all exits, exact int write counts and flushes. Real normal/-O
   healthy/native both failed/diagnostic/help/parser and dirty/closed/absent seams.
3. Review/docs/knowledge. Depends1–2; four assertion mutants and restored passes,
   normal/-O affected suite, compile, existing Bandit, actual ECC self-review/fixes;
   current source/raw receipts, README/security/MIT/research attribution/AI disclosure,
   STATE/DECISIONS/LEARNING, fresh verified Obsidian milestone. No Git/CI added.

Verified commands: python -m unittest discover -s tests -v;
python -O -m unittest discover -s tests -v; python tools/check_mutations.py;
python -m compileall -q lifecycle_lab tests tools; python -m bandit -r lifecycle_lab tools
-f json; python -m lifecycle_lab demo. Use installed runtime/tools only; no arbitrary
coverage target. Core forbidden-host-call tests after trusted harness imports.

Not authorized: actual links/unlink/rename/open/stat/chmod/chown/identity/ACL/path
traversal, disk/file experiments, real/private target data, VM/services/root/installs,
upstream execution, general filesystem/dup/fork/mmap/async/descriptor reuse, permission
or recovery engine, secure deletion, new repository/CI/publication/push/merge/deploy/
chats/subagents/schedulers/reply loops/spending, parent/shared/accepted lab edits.
Research artifacts are ordinary owned documentation/source evidence only. Prior
Linux/live/hosted/secret-history/resource/manual limitations remain unchanged.

Completion: approved stages1-3 locally complete;31 normal/O tests,70 actual child
observations each,22 unchanged full reports,32trace/150snapshot domain, four assertion
mutants/restoration, compile/app-tools Bandit and both demos/stress pass. Measured
admitted width46,792 bytes below conservative163840; not a global optimum proof.
First evidence-capture harness restoration failure retained/fixed/rechecked; exact
results/platform/scanner limits in VERIFICATION/REVIEW and research receipts.
