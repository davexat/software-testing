# Kiwi TCMS — Live Demo Script (15 minutes, 2 speakers)
**Group 4 — Tool type: Test Management**

Stage directions in *[brackets]*. Spoken text plain. Pace ≈ 135 words/minute.
**A** = speaker 1 (planning side). **B** = speaker 2 (execution and reporting side).
Every live action below was rehearsed against the instance in this repository.

| Block | Who | Time |
|---|---|---|
| 1. The problem and the tool | A | 0:00 → 3:00 |
| 2. Planning: product, plan, cases | A | 3:00 → 7:15 |
| 3. Execution: runs, results, defects | B | 7:15 → 11:00 |
| 4. Automation and reporting | B | 11:00 → 14:15 |
| 5. Benefits, limits, repo, close | A + B | 14:15 → 15:00 |

---

## BLOCK 1 — A — The problem and the tool (0:00 → 3:00)

*[Slide 1: title]*

Good morning. We are Group 4. Our assigned tool type is **test management**, and the tool we investigated is **Kiwi TCMS**.

Let me start with the problem, because test management is the one category in this course that is not about *executing* a test — it is about **controlling the process around the tests**.

*[Slide 2: a spreadsheet with a red cross over it]*

Picture a team with five testers, two supported versions, and four hundred test cases. Four questions decide whether you can ship:
Which cases are actually in scope for this release?
Who is responsible for each one?
Against **which build** were they executed?
And when one failed, where is the evidence and the defect it produced?

Most teams answer that with a spreadsheet. A spreadsheet does not version, it cannot link a failure to a bug, it cannot tell you who changed an expected result last Tuesday, and it cannot merge manual results with automated ones. That gap is what a test management tool fills.

*[Slide 3: what it is]*

**Kiwi TCMS** is a free, open-source, self-hosted test case management system. Python and Django, GPL version two, deployed as a Docker container with a MariaDB database. It descends from Red Hat's Nitrate project and it is actively maintained.

Its **aim**, in one sentence: to give a team one traceable, auditable place where the whole testing process lives — planning, execution, and reporting — with no licence cost and no test data leaving your infrastructure.

*[Switch to browser: https://localhost:8443, already logged in, dashboard]*

This is a live instance running in Docker on this laptop. Look at the menu, because that vocabulary **is** the process model: **Test Plans, Test Cases, Test Runs**, and under them Products, Versions and Builds. I will build the left half of that model now; my colleague will execute it.

---

## BLOCK 2 — A — Planning: product, plan, cases (3:00 → 7:15)

*[Browser: Products]*

Test management starts by declaring **what is under test**. In Kiwi that is a **Product**, which owns **Versions**, **Builds** and **Components**.

*[Open "Solinal Demo Shop"]*

Our demo product is a small shop application, version one-point-two, build forty-five. This is not paperwork — it is what later lets us say a test passed **on build forty-five**, which is the difference between a result and a *traceable* result.

*[Testing → Test Plans → open "Regression - Authentication 1.2"]*

Next, the **Test Plan**: the scope and strategy for a product and a version. It has a type — ours is *Regression* — a text section with the scope and the exit criteria, and it owns a set of test cases. When version one-point-three starts, you clone the plan instead of rewriting it.

*[Scroll to the case list inside the plan]*

Here is the **case library**. Every column is a management decision, not a technical one: **priority**, **category**, **automation status**, **default tester**. This is how a lead decides what to run when there are two days left and four hundred cases — filter by P1 and run those first.

*[Open the case "Login with an expired password is rejected"]*

A **Test Case** is a reusable asset: preconditions, steps, expected result, and a `script` field that links it to the automated test that covers it. Notice it exists **independently of any execution** — the same case can live in the smoke plan, the regression plan, and three versions at once, with no copy-paste.

*[Click "New Test Case" — create ONE live, text from docs/snippets.md]*

Let me add one live. Summary: *"Session expires after 30 minutes of inactivity"*. Category Functional, priority P2, status Confirmed. Steps and expected result — paste. Save. And add it to the regression plan.

*[Open the case History tab]*

One detail that matters for management rather than for testing: **every change is versioned**. Kiwi keeps who changed which field and when. In an audited project, that history *is* a deliverable.

So we now know what we test, how important each case is, and who owns it. Nothing has been executed yet.

---

## BLOCK 3 — B — Execution: runs, results, defects (7:15 → 11:00)

*[Browser: Testing → Test Runs → "Manual regression - build-45"]*

Thank you. A plan is a *definition*. A **Test Run** is an *event*: it takes the cases of a plan and pins them to one build, one manager, one assigned tester.

*[Point at the execution rows]*

Inside the run are **Test Executions** — one row per case in this run, each with its own status: idle, running, passed, failed, blocked. That means one test case can hold twenty different results across twenty runs, and every one of them is preserved with its build and its date.

That separation between **case** and **execution** is the core idea of test management, and it is exactly what a spreadsheet cannot represent.

*[Execute: mark three executions PASSED]*

I am the assigned tester, so I execute and I record. Passed. Passed. Passed.

*[Mark "Login with an expired password is rejected" as FAILED, add a comment]*

This one fails: the password was ninety-one days old and the system still let the user in. I set the status to **failed** and I add a comment with what I observed. That comment is the evidence trail.

*[Open the execution's Bugs tab and attach the defect link]*

Now I close the loop with the defect. Kiwi integrates with issue trackers — GitHub, JIRA, Bugzilla, Redmine — so a failed execution can open a pre-filled issue containing the case, its steps and the build, and keep it linked. Here is that defect, permanently attached to this execution.

*[Show the run's progress bar / status summary]*

And at the top of the run: how many passed, failed, blocked, still idle. That is the release-readiness number a manager actually asks for.

The full chain now reads: **plan → case → run → execution → defect**, on a named build. Answering "what proves we tested login on build forty-five, and what happened" takes three clicks instead of an archaeology dig through a shared drive.

---

## BLOCK 4 — B — Automation and reporting (11:00 → 14:15)

*[Terminal beside the browser]*

Everything so far was manual. But most teams also have automated tests, and a management tool that ignores them splits the picture in two again. Kiwi solves that with a **JSON-RPC API**, an official Python client, and plugins for pytest, JUnit XML and TAP.

*[Run: `.venv/bin/python -m pytest --junitxml=junit.xml`]*

This is the automated suite for the same product. Four tests pass, one fails — the same expired-password defect, deliberately left in the code.

*[Run: `.venv/bin/python automation/report_results.py junit.xml`]*

And this script sends that report into Kiwi through the API.

*[Switch to browser, refresh Test Runs]*

Look at what happened on the server: a **new test run was created automatically**, on the same product, plan and build, with one execution per case and the real status of each. No manual data entry, and every automated test is matched to the managed test case that describes it — anything unmatched is reported, never silently dropped.

*[Telemetry → Testing status matrix, then Execution trends]*

Which brings us to reporting. Under **Telemetry**, Kiwi ships dashboards built for management questions rather than for debugging: the *testing status matrix*, showing which cases pass or fail across builds; *execution trends* over time; and breakdowns by tester, priority and component. This is where you notice that one component fails repeatedly across three builds — a pattern that is invisible inside any single test result.

---

## BLOCK 5 — A + B — Benefits, limits, repo, close (14:15 → 15:00)

**A** *[Slide: benefits]*

To summarise the **benefits**, specifically as a *test management* tool:

- **Free and self-hosted** — TestRail or Zephyr charge per user per month; Kiwi is GPL and your test data stays on your infrastructure.
- **One source of truth** for manual and automated results.
- **Traceability** from plan to case to run to defect, with full change history for audits.
- **Process structure out of the box** — roles, assignments, notifications — so a team of ten does not have to invent conventions.

And honestly, the **limits**: the interface looks dated, someone has to administer and back up the instance, and community support is best-effort — the project is funded by a paid hosted edition.

**B** *[Slide: repo URL + QR]*

Everything you saw is reproducible. Our public repository has the Docker Compose file, the seed script that creates the product, plan and cases through the API, the pytest suite, the results importer, and a README that gets you to this exact state. The link is on screen and in the virtual classroom.

**A**

Closing thought: the other tools in this course make tests *run*. Kiwi TCMS makes the testing **accountable** — it turns a pile of results into a defensible answer to "can we release this build?".

Thank you. Questions?

---

## Q&A ammunition (30–60 s each)

- **"Why not Jira with Xray or Zephyr?"** — those are paid Jira plugins, priced per user. Kiwi is standalone and free, and it *integrates* with Jira as an issue tracker instead of requiring it.
- **"Does it run the tests?"** — No, and that is the point. Execution comes from testers or from CI; results flow in through the API or the plugins.
- **"Requirements traceability?"** — Cases carry a requirement reference, and the plan-per-version structure gives coverage per release.
- **"How does it scale?"** — Django plus a relational database; public instances handle tens of thousands of cases. The real limit is process discipline, not the tool.
- **"Adoption effort?"** — Under a day for the instance and the product setup. The real cost is writing the case library, which you pay with any tool.
- **"Can it plug into CI?"** — Yes: our importer is ~100 lines against the API, and official plugins exist for pytest, JUnit XML and TAP.
