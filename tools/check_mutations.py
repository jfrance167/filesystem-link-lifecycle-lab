"""Four in-memory faults require assertions/zero errors and restored passes.

Usage: python tools/check_mutations.py. No source changes or external commands;
raw failure/restoration traces are output, not a mutation-coverage score.
"""
from io import StringIO
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/"tests"))
from lifecycle_lab import core
from test_core import CoreTests


def run_case(name):
    result=unittest.TextTestRunner(stream=StringIO()).run(unittest.TestSuite([CoreTests(name)]))
    return {"passed":result.wasSuccessful(),"assertion_failures":len(result.failures),"errors":len(result.errors),
            "tests_run":result.testsRun,"failure_evidence":[detail for _,detail in result.failures],
            "error_evidence":[detail for _,detail in result.errors]}


def main():
    apply=core._apply
    def unlink_all(names,event):
        target=names[event["name"]]
        for name in list(names):
            if names[name]==target: del names[name]
    def close_all(refs,event):
        target=refs[event["reference_id"]]
        for ref in list(refs):
            if refs[ref]==target: del refs[ref]
    def retarget(names,refs,used,event):
        apply(names,refs,used,event)
        if event["op"]=="link":
            for ref in refs: refs[ref]=names[event["new_name"]]
    pairs=(("ignored_references","_eligible",lambda names,refs:names==0,"test_open_retention_regression"),
           ("unlink_all_names","_unlink",unlink_all,"test_one_name_regression"),
           ("close_all_references","_close",close_all,"test_one_reference_regression"),
           ("retarget_on_link","_apply",retarget,"test_rebind_regression"))
    results=[]
    for name,target,fault,test in pairs:
        with patch.object(core,target,fault): result=run_case(test)
        results.append({"mutation":name,**result,"detected":result["assertion_failures"]>0 and result["errors"]==0})
    restored=[run_case(test) for _,_,_,test in pairs]
    print(json.dumps({"mutations":results,"restored":restored,"scope":"four in-memory logic faults; no source edits"},indent=2))
    return 0 if all(item["detected"] for item in results) and all(item["passed"] for item in restored) else 1


if __name__=="__main__":
    raise SystemExit(main())
