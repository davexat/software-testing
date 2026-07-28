# Clipboard snippets for the live demo

Never type long text on stage. Keep this file open in a second window and copy from it.

## The Test Case created live in Block 2

**Summary**

```
Session expires after 30 minutes of inactivity
```

**Text (steps and expected result)**

```
**Preconditions:** a user with an active session.

1. Log in and stay idle for 31 minutes.
2. Trigger any authenticated action.
**Expected:** the session is rejected and the user is sent back to the login screen.
```

Category: `--default--` · Priority: `P2` · Status: `CONFIRMED` · Automated: no

## The comment added to the FAILED execution in Block 3

```
Password was 91 days old (max age is 90) and login still succeeded.
No 'password expired' error was shown. Reproduced on build-45.
```

## Commands for Block 4

```
.venv/bin/python -m pytest --junitxml=junit.xml
.venv/bin/python automation/report_results.py junit.xml
```

## Environment (run before the demo, in every terminal you will use)

```
set -a; source .env; set +a
```
