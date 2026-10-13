# Kyber PQC KEM Engine

**Rule-based telemetry demonstration.** This repository evaluates numerical thresholds, descriptor keywords, and critical flags through Python CLI/API workflows and a static browser console.

> **Security scope:** Despite its historical name, this project **does not implement ML-KEM (Kyber)** key generation, encapsulation, decapsulation, NTT arithmetic, hybrid TLS, FIPS 203 test-vector validation, or cryptographic module certification. It must not be used to establish keys, protect traffic, or assert post-quantum security. See [NIST FIPS 203](https://csrc.nist.gov/pubs/fips/203/final) for the actual ML-KEM specification.

## Functionality

- Deterministic threshold alerts, descriptor anomaly detection, and critical-flag escalation
- Python CLI for single evaluations, CSV batch processing, deterministic mock chat, in-memory HMAC audit verification, and a FastAPI server
- Separate legacy package CLI and numerical enrichment demonstrations (not cryptographic benchmarks or conformance testing)
- Browser-only telemetry form in **web/index.html**, with JSON export and no network requests
- HMAC-SHA256 hash-chained audit records held in **process memory only**; no durable storage or external anchoring

The root evaluator flags primary metric greater than **25**, secondary metric greater than **12**, and descriptor keywords such as DISCORDANT, ANOMALY, MUTANT, VIOLATION, FAIL, or REJECT. A critical flag takes priority. These are *demonstration heuristics*, not NIST standards. The legacy package CLI uses a secondary limit of **10**.

## Browser demonstration

Open **web/index.html** directly in a modern desktop or mobile browser. Enter numeric metrics, select **Evaluate**, and optionally **Export JSON**. The app validates finite numbers and clearly distinguishes simulated rule decisions from cryptographic security assessments.

The Pages workflow at **.github/workflows/pages.yml** can publish the static web directory when GitHub Pages has been configured with **GitHub Actions** as its source. A public URL should only be published after verifying deployment.

**Privacy:** Browser inputs remain local, and no results are persisted after reload. Avoid identifiable personal data and secrets. The Python API is unauthenticated; bind it to loopback or protect it with an authentication gateway if exposing it beyond a trusted host. The regex-based identifier filter is not a HIPAA de-identification guarantee.

## Installation and usage

CI tests Python 3.10, 3.11, and 3.12. Package metadata allows Python >=3.9, but CI does not separately test 3.9.

~~~bash
git clone https://github.com/abusuraihsakhri/kyber-pqc-kem-engine.git
cd kyber-pqc-kem-engine
python -m pip install -e ".[server,test]"
kyber-pqc-kem-engine audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
kyber-pqc-kem-engine chat "status"
kyber-pqc-kem-engine batch -i sample.csv -o results.csv
kyber-pqc-kem-engine verify-audit
kyber-pqc-kem-engine serve --host 127.0.0.1 --port 8000
~~~

The installed command invokes the **root CLI**, matching python cli.py. For the independent legacy workflow, run python -m kyber_pqc_kem.cli.

CSV columns: task_id, target_identifier, primary_metric, secondary_metric, status_descriptor, is_critical_flag. Boolean values accept true/false, 1/0, yes/no, or blank (false); invalid values are rejected. Batch input and output paths must differ.

With the server running, browse http://127.0.0.1:8000/docs for interactive API documentation. Endpoints include /health, /metrics (JSON), /api/audit, /api/chat (local mock), and /api/audit/logs. No external model provider is implemented. Audit-chain verification is limited to records in the *current running process*; a fresh CLI invocation has an empty chain.

## Configuration and security

The audit HMAC secret is read from the AUDIT_SECRET_KEY environment variable. If unset, a random process-local key is used and cannot be recovered after restart. The example .env file is not automatically loaded.

~~~bash
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
python -m cli serve --host 127.0.0.1 --port 8000
~~~

For containers, docker compose up --build requires AUDIT_SECRET_KEY and publishes only to localhost on port 8000. The audit ledger is not a durable evidence store. Do not expose the API publicly without application-layer authentication.

## Tests

~~~bash
python -m pytest -v
python -m compileall -q agents kyber_pqc_kem cli.py enrichment.py simulator.py
node tests/web-smoke.cjs
python simulator.py 100
~~~

CI additionally checks package installation and dependency consistency. The simulator produces synthetic telemetry; it is not a PQC performance benchmark.

## Technology and compatibility

Python, Pydantic v2, optional FastAPI/Uvicorn, HTML/CSS/vanilla JavaScript. The static web interface requires neither Pyodide nor a Python server. GitHub Pages cannot host the Python API.

## License

[MIT](LICENSE).
