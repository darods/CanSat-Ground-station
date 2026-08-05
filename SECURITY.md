# Security Policy

## Supported Versions

Security fixes land on the `master` branch and are released from there.
Patches are back-ported only to the latest tagged release; older tags are
not patched.

| Version / branch        | Supported          |
| ----------------------- | ------------------ |
| `master`                | ✅ Yes             |
| latest tagged release   | ✅ Yes             |
| older tags / branches   | ❌ No              |

## Reporting a Vulnerability

Please **do not open a public issue** for security problems.

Report privately via GitHub's **Private Vulnerability Reporting**
(Repository → Security → Report a vulnerability), which sends the report
directly to the maintainers without exposing it publicly.

If you are a maintainer and prefer an e-mail contact instead, add it below
and mention it in the README:

> Security contact: <you@example.com>

### What to include

- A minimal description of the bug and why it is a security issue.
- Steps to reproduce, or a small proof-of-concept (payload/input).
- The affected component (e.g. `communication.py` serial parsing,
  `graphs/` data handling, `dataBase.py` CSV export).
- Any fix suggestion if you have one.

You should receive an acknowledgement within 5 business days. We will keep
you updated on the fix and, once released, credit you unless you prefer to
stay anonymous.

## Security practices in this project

- **CI (free tier, public repo):** `pip-audit` checks dependencies for known
  CVEs, `bandit` scans source for common vulnerability classes, and GitHub
  CodeQL runs semantic analysis weekly and on every PR.
- **Dependabot:** dependency version bumps and automated PRs for
  vulnerabilities are opened automatically.
- **Input hardening:** telemetry frames are validated before display —
  non-finite values (NaN/inf) are rejected, serial reads are length-capped,
  and CSV export neutralizes spreadsheet formulas (`=`, `+`, `@`).
- **Secrets:** never commit credentials or API keys. Secret scanning + push
  protection should stay enabled on this repository.
