#!/usr/bin/env python3
"""Push a pytest JUnit XML report into Kiwi TCMS as a Test Run.

This is the "automation ingestion" half of the demo: automated results end up in
the same product, plan and build as the manual ones, so a single report answers
"is this build ready?".

    pytest --junitxml=junit.xml
    python automation/report_results.py junit.xml

Each <testcase name="..."> is matched to a Test Case whose `script` field holds
that same name. Unmatched tests are reported and skipped, never silently dropped.
"""

import pathlib
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from automation.kiwi import (  # noqa: E402
    BUILD,
    PLAN,
    connect,
    current_username,
    first,
)


def parse_junit(path: pathlib.Path) -> list[dict]:
    root = ET.parse(path).getroot()
    results = []
    for node in root.iter("testcase"):
        failure = node.find("failure")
        error = node.find("error")
        skipped = node.find("skipped")
        if failure is not None:
            status, detail = "FAILED", failure.get("message", "")
        elif error is not None:
            status, detail = "ERROR", error.get("message", "")
        elif skipped is not None:
            status, detail = "WAIVED", skipped.get("message", "")
        else:
            status, detail = "PASSED", ""
        results.append(
            {
                "name": node.get("name"),
                "classname": node.get("classname", ""),
                "status": status,
                "detail": detail,
            }
        )
    return results


def main() -> None:
    report = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "junit.xml")
    if not report.exists():
        sys.exit(f"{report} not found. Run: pytest --junitxml={report}")

    results = parse_junit(report)
    print(f"Parsed {len(results)} results from {report}")

    rpc = connect()
    plan = first(rpc.TestPlan.filter({"name": PLAN}), f"test plans named '{PLAN}'")
    build = first(rpc.Build.filter({"name": BUILD}), f"builds named '{BUILD}'")
    user = first(rpc.User.filter({"username": current_username()}), "users")

    by_script = {
        case["script"]: case
        for case in rpc.TestCase.filter({"plan": plan["id"]})
        if case.get("script")
    }
    statuses = {s["name"]: s["id"] for s in rpc.TestExecutionStatus.filter({})}

    run = rpc.TestRun.create(
        {
            "summary": f"Automated regression (pytest) - {BUILD}",
            "plan": plan["id"],
            "build": build["id"],
            "manager": user["id"],
            "default_tester": user["id"],
            "notes": f"Imported from {report.name} by automation/report_results.py",
        }
    )
    print(f"Created test run {run['id']}: {run['summary']}")

    unmatched = []
    for result in results:
        case = by_script.get(result["name"])
        if case is None:
            unmatched.append(result["name"])
            continue

        # TestRun.add_case returns one execution per case-and-build combination.
        added = rpc.TestRun.add_case(run["id"], case["id"])
        executions = added if isinstance(added, list) else [added]

        for execution in executions:
            rpc.TestExecution.update(
                execution["id"],
                {"status": statuses[result["status"]], "tested_by": user["id"]},
            )
            if result["detail"]:
                rpc.TestExecution.add_comment(
                    execution["id"], f"pytest: {result['detail']}"
                )
        print(f"  {result['status']:7} {case['summary'][:50]}")

    if unmatched:
        print("\nNot linked to any managed test case (add the name to `script`):")
        for name in unmatched:
            print(f"  - {name}")

    print(f"\nOpen https://localhost:8443/runs/{run['id']}/")


if __name__ == "__main__":
    main()
