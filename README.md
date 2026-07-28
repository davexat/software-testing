# Test Management with Kiwi TCMS — Group 4 Demo

Tool type (lottery): **Test management**. Tool investigated: **[Kiwi TCMS](https://kiwitcms.org/)**, a free, open-source, self-hosted test case management system (GPLv2+, Python/Django).

This repository reproduces the full state of our live demo: a Kiwi TCMS instance, a demo product with a test plan and test cases, a small system under test with a pytest suite, and a script that pushes the automated results back into Kiwi as a Test Run.

> Kiwi TCMS does not run tests — it **manages** them. That is exactly the point of this demo: it is the layer that turns individual test results into a traceable, auditable answer to *"is this build ready to release?"*.

---

## What is in here

| Path | What it is |
|---|---|
| `docker-compose.yml` | The Kiwi TCMS instance (web + MariaDB) |
| `seed/seed_demo.py` | Creates the demo fixture over the API: Product → Version → Build → Test Plan → 6 Test Cases → Test Run |
| `app/auth.py` | The system under test — authentication rules, with one deliberate defect |
| `tests/test_auth.py` | pytest suite: 4 tests pass, 1 fails (the defect) |
| `automation/report_results.py` | Imports a pytest JUnit XML report into Kiwi as a Test Run with real statuses |
| `automation/kiwi.py` | Shared API connection helpers and the fixture constants |
| `demo-script.md` | The 15-minute presentation script |

## The object model this demo walks through

```
Product (Solinal Demo Shop)
└── Version 1.2
    └── Build build-45
Test Plan  "Regression - Authentication 1.2"   ← scope and strategy
└── Test Case  (reusable, prioritised, versioned)
    └── Test Execution   ← one case, in one run, on one build, by one tester
        └── status + comments + linked defect
Test Run  = plan's cases × a build × a tester      ← the executable campaign
Telemetry = the release-readiness report
```

---

## Reproduce it

Requirements: Docker with the Compose plugin, Python 3.10+.

### 1. Start Kiwi TCMS

```bash
docker compose up -d
docker compose exec web python manage.py migrate
docker compose exec -e DJANGO_SUPERUSER_PASSWORD=demo-password-123 web \
  python manage.py createsuperuser --noinput --username admin --email admin@example.com
```

Open **https://localhost:8443** and accept the self-signed certificate warning.
Log in as `admin` / `demo-password-123`.

> Port 8080 only redirects to HTTPS — the application is served on 8443.
> No Compose plugin? See [Without Docker Compose](#without-docker-compose) below.

### 2. Install the Python side

```bash
python -m venv .venv
source .venv/Scripts/activate
(.venv) pip install -r requirements.txt
cp .env.example .env
set -a; source .env; set +a
```

### 3. Create the demo fixture

```bash
(.venv) python seed/seed_demo.py
```

```
Connected to Kiwi TCMS
  + created classification 'Web'
  + created product 'Solinal Demo Shop' (id=1)
  + created version 1.2 (id=2)
  + created build build-45 (id=3)
  + created test plan 'Regression - Authentication 1.2' (id=1)
  + created case 'Login with valid credentials returns a s...'
  ...
  + created test run (id=1) with all executions IDLE
```

The script is idempotent — re-running it will not duplicate anything.

### 4. Run the automated suite and publish the results

```bash
(.venv) python -m pytest --junitxml=junit.xml     # 4 passed, 1 failed (on purpose)
(.venv) python automation/report_results.py junit.xml
```

```
Parsed 5 results from junit.xml
Created test run 2: Automated regression (pytest) - build-45
  PASSED  Login with valid credentials returns a session tok
  PASSED  Login with a wrong password is rejected
  PASSED  Account is locked after 3 consecutive failed attem
  PASSED  A disabled account cannot log in
  FAILED  Login with an expired password is rejected
```

Open the run in Kiwi: the automated results now sit next to the manual ones, on the same product, plan and build.

### 5. See the reports

**Telemetry → Testing status matrix** and **Execution trends** in the Kiwi menu.

---

## How the results are matched

Each `<testcase name="...">` in the JUnit report is matched to the Test Case whose **`script`** field contains that test name. Anything unmatched is printed at the end of the import and skipped — never silently dropped.

To automate a new case: set its `script` field in Kiwi to the pytest test function name.

Kiwi also publishes official plugins (`kiwitcms-junit.xml-plugin`, `kiwitcms-pytest-plugin`, TAP) that do the same job. We wrote our own importer here so that the demo also shows the **JSON-RPC API**, which is the extension point behind all of those plugins.

---

## The deliberate defect

`app/auth.py::is_password_expired` compares against `PASSWORD_MAX_AGE_DAYS + 1`, so a password exactly one day past the maximum age is still accepted. `test_login_with_expired_password_is_rejected` catches it, which gives the demo a real FAILED execution to triage and report as a defect.

Fix it by changing the comparison to `> PASSWORD_MAX_AGE_DAYS` — the suite then goes fully green, which is useful for showing an execution-trend change across two builds.

---

## Without Docker Compose

```bash
docker network create kiwi_net
docker run -d --name kiwi_db --network kiwi_net --network-alias db \
  -e MARIADB_ROOT_PASSWORD=kiwi -e MARIADB_DATABASE=kiwi \
  -e MARIADB_USER=kiwi -e MARIADB_PASSWORD=kiwi mariadb:10.11
docker run -d --name kiwi_web --network kiwi_net -p 8080:8080 -p 8443:8443 \
  -e KIWI_DB_HOST=db -e KIWI_DB_PORT=3306 -e KIWI_DB_NAME=kiwi \
  -e KIWI_DB_USER=kiwi -e KIWI_DB_PASSWORD=kiwi kiwitcms/kiwi:latest
docker exec kiwi_web /Kiwi/manage.py migrate
```

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `Table 'kiwi.auth_user' doesn't exist` | Migrations have not run yet — `docker compose exec web /Kiwi/manage.py migrate` |
| `SSL: CERTIFICATE_VERIFY_FAILED` | Self-signed certificate — keep `TCMS_INSECURE_SSL=1` set (local demo only) |
| `Unrecognized URL scheme` | `TCMS_API_URL` must include the scheme and end in `/xml-rpc/` |
| Browser stuck on `http://localhost:8080` | The app is on **https**://localhost:**8443** |
| `returned no categories` | The product was created without its default category — delete it in the admin and re-run the seed |

## Licence and credit

Kiwi TCMS is © the Kiwi TCMS project, GPLv2+. This repository is coursework built on top of it.
