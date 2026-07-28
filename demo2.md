### Kiwi TCMS — Live Demo Script (10–15 minutes, 5 presenters)

**Group 4 — Tool Type: Test Management**

---

# Technical Glossary

Before we begin, here are the technical terms we will use during the presentation.

| Term                | Meaning                                                                                                                                                                                                                        |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Build**           | A specific version of the software that was built for testing. For example, **build-45** is version 45 of the product. Every time developers make changes and compile the code, a new build is created and needs to be tested. |
| **Test Case**       | A testing scenario that describes what should be verified. It includes steps, an expected result, and a priority. Example: *"Login with a valid password returns a token."*                                                    |
| **Test Plan**       | A collection of test cases organized under a testing strategy. It defines what will be tested, against which version, and the exit criteria.                                                                                   |
| **Test Run**        | A specific execution of the test cases in a test plan against a particular build, with the results recorded. It represents the actual testing event.                                                                           |
| **Test Execution**  | One execution record inside a Test Run. It contains a test case, its result (PASSED, FAILED, BLOCKED), the tester who executed it, and the build that was tested.                                                              |
| **Test Management** | Test management is not about running tests. It is about organizing the testing process: knowing what was tested, who tested it, which build was tested, what failed, and where the evidence is stored.                         |

---

# BLOCK 1 — Presenter 1 — The Problem Kiwi TCMS Solves (0:00 → 2:00)

*[Slide: Group title and tool name]*

Good morning. We are **Group 4**, and today we will present **Kiwi TCMS**, an open-source test management system.

*[Slide: Spreadsheet image with a red X]*

Before looking at the tool, let's understand the problem it solves.

Imagine a team with five testers, two software versions, and four hundred test cases. Before releasing the software, the team needs to answer four important questions.

Which test cases are included in this release? Who is responsible for each one? Which build were they executed against? And if a test failed, where is the evidence and the related bug report?

Many teams try to manage all of this with spreadsheets. However, spreadsheets have important limitations. They cannot track changes over time, they cannot link failed tests to bug reports, they cannot show who modified a test case, and they cannot combine manual and automated test results in one place.

This is exactly the problem that a test management tool solves.

Kiwi TCMS does **not** execute tests. Instead, it **organizes the testing process and provides full traceability**.

---

# BLOCK 2 — Presenter 2 — Understanding the Product Structure (2:00 → 4:30)

*[Open Kiwi TCMS in the browser at https://localhost:8443, already logged in]*

In Kiwi, everything starts by defining **what is being tested**.

The structure is hierarchical, and understanding it makes the rest of the tool much easier to follow.

First, we have the **Product**. The product represents the software being tested. In our example, we have **Solinal Demo Shop**, a small online store.

Each product has one or more **Versions**. Our current version is **1.2**. When version 1.3 is released, we simply create a new version instead of replacing the old one.

Next comes the **Build**.

A build is a specific compiled version of the software. Every time developers make changes and compile the application, they produce a new build.

In our demo, we are testing **build-45**.

Testing against a specific build means we always know exactly which version of the code produced the testing results.

*[Point to the Test Plan information with the mouse]*

This information is very important because later we can clearly say that a test **passed on build-45**. That is what makes the result traceable.

Finally, we have the **Test Plan**.

A Test Plan defines the testing strategy. It specifies which test cases belong to the plan, which product version they are for, and the exit criteria.

For example, our exit criterion could be that all **Priority 1** test cases must pass before the release.

When version 1.3 becomes available, we can simply clone this plan instead of creating everything again.

---

# BLOCK 3 — Presenter 3 — Creating and Reviewing Test Cases (4:30 → 7:00)

*[Inside the Test Plan, show the list of test cases]*

Now let's look at the **Test Cases**.

A Test Case is a reusable testing asset. It contains the preconditions, the test steps, the expected result, and it can also be linked to an automated test.

An important point is that a Test Case exists independently from any execution.

The same test case can belong to different test plans, such as a smoke test plan and a regression test plan, and it can also be reused across multiple software versions.

Each management field helps organize the testing process.

For example, **Priority** tells us which tests are the most critical. A Priority 1 test is more important than a Priority 2 test.

We also have categories and assigned testers.

This allows a test lead to quickly filter the most critical test cases when there is limited time before a release.

*[Open "Login with an expired password is rejected"]*

Here we can see the test steps and the expected result.

Now we will create a new test case.

The summary is **Session expires after 30 minutes of inactivity**.

We select the product **Solinal Demo Shop**, choose the default category, keep the status as **Confirmed**, set the priority to **P2**, and leave automation disabled.

Then we enter the following information:

> **Preconditions:** A user with an active session.
>
> 1. Log in and stay idle for 31 minutes.
> 2. Trigger any authenticated action.
>
> **Expected Result:** The session is rejected and the user is redirected to the login screen.

We save the changes and manually add the new test case to our Test Plan.

---

# BLOCK 4 — Presenter 4 — Manual Execution and Bug Tracking (7:00 → 9:30)

*[Open Testing → Test Runs → "Manual regression - build-45"]*

A Test Plan is only a definition.

A **Test Run** is the actual testing event.

It takes the test cases from a plan and executes them against a specific build with assigned testers.

*[Point to the execution rows]*

Inside the Test Run, we have the **Test Executions**.

Each row represents one execution of one test case.

Every execution has its own status, such as **Idle**, **Running**, **Passed**, **Failed**, or **Blocked**.

The same Test Case can appear in many Test Runs, and each execution keeps its own result, build, and execution date.

This separation between **Test Case** and **Test Execution** is one of the key ideas of test management, and it is something that spreadsheets cannot represent well.

*[Mark three executions as PASSED]*

As the assigned tester, I execute these test cases and record the results.

This one passed.

This one passed.

And this one also passed.

*[Mark "Login with an expired password is rejected" as FAILED and add the comment]*

Now let's suppose this test fails.

We add the following comment:

> Password was 91 days old (max age is 90) and login still succeeded. No "password expired" error was shown. Reproduced on build-45.

Then we mark the execution as **Failed**.

*[Open the Bugs tab and link the defect]*

Kiwi TCMS integrates with issue tracking systems such as **JIRA** and **Bugzilla**.

A failed execution can be linked directly to a bug report, keeping the test case, the testing steps, and the build connected to the issue.

*[Show the progress bar]*

At the top of the Test Run, we can immediately see how many tests passed, failed, are blocked, or are still waiting to be executed.

This is exactly the information a project manager needs when deciding whether the software is ready for release.

---

# BLOCK 5 — Presenter 5 — Automation, Reports, and Conclusion (9:30 → 12:00)

*[Open the terminal next to the browser]*

Everything we have shown so far was done manually.

However, most software projects also use automated tests, and a good test management tool should support them as well.

Kiwi TCMS provides a **JSON-RPC API**, an official **Python client**, and plugins for **pytest**, **JUnit XML**, and **TAP**.

For this demo, we wrote a small importer of about one hundred lines to demonstrate how the API works.

*[Run `python -m pytest --junitxml=junit.xml`]*

Here we execute the automated test suite for the same application.

Four tests pass, and one test fails.

The failed test is the same expired password defect that we intentionally left in the application.

*[Run `python automation/report_results.py junit.xml`]*

This script sends the test results to Kiwi TCMS through its API.

*[Refresh the Test Runs page]*

Now look at what happened.

A **new Test Run was created automatically**.

It belongs to the same product, test plan, and build, but it was generated entirely from the automated test results.

Each automated test is linked to its corresponding Test Case, and every execution shows its real result without any manual data entry.

*[Open Telemetry → Testing Status Matrix, then Execution Trends]*

Finally, Kiwi TCMS also includes reporting dashboards under the **Telemetry** section.

The **Testing Status Matrix** shows which test cases passed or failed for each build.

The **Execution Trends** report shows testing progress over time.

There are also reports grouped by priority and component.

*[Final slide: Benefits, Limitations, Repository]*

To summarize, Kiwi TCMS offers several advantages as a test management tool.

It is **free and self-hosted**, unlike tools such as **TestRail** or **Zephyr**, which require paid licenses.

It provides a **single source of truth** for both manual and automated testing results.

It offers complete **traceability** from the test plan, to the test case, to the test execution, and finally to the related defect.

It also provides a structured testing workflow with user roles, assignments, and notifications already built in.

Of course, it also has some limitations.

Its user interface looks somewhat outdated, the server must be maintained by your own team, and community support depends on volunteers.

Everything we demonstrated today can be reproduced.

Our public repository includes the Docker Compose configuration, the seed script, the pytest test suite, the results importer, and a README with all the instructions needed to recreate this environment.

To conclude, many testing tools focus on **running tests**.

Kiwi TCMS focuses on **managing the testing process**.

It transforms individual test results into organized, traceable information that helps answer one of the most important questions in software development:

**Is this build ready for release?**
