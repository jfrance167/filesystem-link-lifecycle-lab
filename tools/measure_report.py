"""Reusable admitted max-cardinality/width stress; not a global size optimum proof.

Usage: python tools/measure_report.py. Invented IDs only; no OS filesystem calls.
Outputs request, full report and byte/count metrics; retain stdout as evidence.
"""
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from lifecycle_lab import core


def stress_request():
    files=[f"F{i}"+"x"*22 for i in range(4)]
    names=[f"N{i}"+"x"*22 for i in range(8)]
    refs=[f"R{i}"+"x"*22 for i in range(8)]
    return {"id":"S"+"x"*23,"version":1,"profile":"link_lifetime_v1",
            "files":[{"id":file_id,"kind":"regular"} for file_id in files],
            "names":[{"id":name,"file_id":files[i%4]} for i,name in enumerate(names)],
            "references":[{"id":ref,"file_id":files[i%4]} for i,ref in enumerate(refs)],
            "events":[{"id":f"E{i:02d}"+"x"*21,**({"op":"unlink","name":names[7]} if i%2==0
                       else {"op":"link","source_name":names[0],"new_name":names[7]})} for i in range(24)],
            "context":{"platform":"posix_regular","reference_coverage":"complete_declared",
                       "event_outcomes":"assumed_success","excluded_features":[]}}


def main():
    request=stress_request()
    raw=json.dumps(request,separators=(",",":")).encode()
    report=core.analyze_json(raw)
    payload=core.serialize_report(report)
    print(json.dumps({"scope":"admitted 4files/8names/8refs/24events,24-character IDs; no global optimum claim",
                      "input_bytes":len(raw),"report_bytes":len(payload),"conservative_bound":163840,
                      "output_cap":core.MAX_OUTPUT_BYTES,"complete":report["complete"],"request":request,"report":report}))
    return 0 if report["complete"] and len(payload)<163840<core.MAX_OUTPUT_BYTES else 1


if __name__=="__main__":
    raise SystemExit(main())
