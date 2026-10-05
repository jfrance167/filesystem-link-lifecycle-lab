# Research learning

A name is not file identity. Two hard-link names address the same underlying file;
removing one does not retarget a previously held reference. Rebinding the old name
to another file is a useful controlled demonstration of these distinct mappings.

Reference ownership matters: closing one token must not release other holdings.
Actual descriptor duplication shares an open-file description; this proposed narrow
lab excludes it rather than assuming each descriptor is independent. Mappings,
in-flight operations and external holders are also outside the complete-declaration
assumption. Eligibility is conditional, not actual erasure or reclaimed storage.

Filesystem test libraries can intentionally support real-source fallback/real tests;
an in-memory marketing description is not a hostile-code isolation boundary.
Source inspection and relevant tests matter, but inspected tests were not executed.
The local draft did not supply complete multi-link traces; no draft used as oracle.
That research phase had no implementation/testing results. Approved local stages
now pass31 tests normal/O,22 full frozen reports and32 finite traces/150 snapshots.
Four faults each caused1assertion/0errors; restored checks pass. No real OS result.

I/O cleanup detaches both public sinks; tests must restore both, even when only
stderr is being faulted. An initial capture lost JSON output because its diagnostic
seam left stdout None. Corrected patch scopes plus final identity checks make this
visible; source/model success cannot substitute for trustworthy evidence capture.

Exact count types matter: a float equal to requested length must fail, as must bool,
None and a hook-bearing integer subclass. Actual normal/O children cover those
paths and dirty flush/closed/absent/native-pipe shutdown; partial output can remain.
An admitted wide trace measured46,792 bytes, but no logical width cap is hard RSS/
time containment or a proof of real retention/reclamation/secure erasure.
