# Kyber PQC KEM Engine

> **Domain:** Post-Quantum Cryptography & Zero-Knowledge Architecture
> **Reference Guidelines & Standards:** `NIST FIPS 203/204/205, NIST SP 800-90B & ISO/IEC Standards`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Kyber PQC KEM Engine** is an advanced analytical and computational platform implementing NIST FIPS 203 ML-KEM (Kyber-512/768/1024) lattice-based polynomial arithmetic & hybrid X25519-Kyber key exchange.

The system provides a multi-agent evaluation framework with specialized workers for quality control, safety escalation, and protocol conformance monitoring.

---

## ⚙️ Key Capabilities & Algorithmic Modules

- **Deterministic Calculation Engine**: Strict compliance with standard reference formulations and thresholds.
- **Risk & Urgency Classification**: Multi-tier categorization with automated clinical/operational action recommendations.
- **Validation & Guardrails**: Rigorous input bounds checking and anomaly detection.
- **Zero-PHI Outbound Interceptor**: Active regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
- **Tamper-Evident HMAC-SHA256 Audit Trail**: Chained, cryptographically signed logs with full signature verification.

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/kyber-pqc-kem-engine.git
cd kyber-pqc-kem-engine

# Install dependencies
pip install fastapi uvicorn pydantic pytest

# (Optional) Copy environment configuration
cp .env.example .env
# Edit .env to set your AUDIT_SECRET_KEY
```

---

## 💻 CLI Quickstart & Usage

### 1. Run Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Interactive Chat Query
```bash
python cli.py chat "What is the system status?"
```

### 3. Batch Process CSV Records
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch FastAPI REST Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Parameter Reference
- `--task-id`: Unique task identifier (default: TASK-2026-001)
- `--target`: Target entity identifier (default: KEY-TARGET-01)
- `--primary`: Primary measurement value (float, default: 28.5)
- `--secondary`: Secondary measurement value (float, default: 14.2)
- `--critical`: Flag for critical/emergency status (default: False)
- `--status`: Status descriptor (default: DISCORDANT)

### Input Data Schema (CSV Batch)

| Field | Description | Requirement |
|:------|:------------|:------------|
| `task_id` | Parameter / observation metric | Required |
| `target_identifier` | Parameter / observation metric | Required |
| `primary_metric` | Primary measurement value | Required |
| `secondary_metric` | Secondary measurement value | Optional |
| `is_critical_flag` | Emergency escalation flag | Optional |
| `status_descriptor` | Status code descriptor | Optional |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs with full signature verification for every evaluation and state transition.
* **Secure Key Generation:** Cryptographically secure random key generation when no explicit key is configured.
* **Path Traversal Protection:** Input file paths are validated and resolved safely.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

### Environment Variables

| Variable | Description | Required |
|:---------|:------------|:---------|
| `AUDIT_SECRET_KEY` | Secret key for HMAC-SHA256 audit signing (min 32 bytes recommended) | Recommended |
| `MODEL_PROVIDER` | LLM provider for chat features (mock, ollama, claude, openai) | No (default: mock) |
| `API_HOST` | API server bind address | No (default: 127.0.0.1) |
| `API_PORT` | API server port | No (default: 8000) |

Generate a secure audit key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 1000
```

---

## 🐳 Container Deployment

```bash
# Build and run with Docker Compose
AUDIT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))") docker-compose up -d

# Or build and run manually
docker build -t kyber-pqc-kem-engine .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY=your-secure-key kyber-pqc-kem-engine
```

---

## 📁 Project Structure

```
kyber-pqc-kem-engine/
├── agents/                  # Enterprise analytical suite
│   ├── api.py              # FastAPI REST endpoints
│   ├── base.py             # Security, PHI guard, audit trail
│   ├── models.py           # Pydantic data models
│   ├── supervisor.py       # Multi-agent orchestrator
│   ├── workers.py          # Specialized evaluation workers
│   ├── llm_factory.py      # LLM provider factory
│   ├── learning.py         # Bayesian calibration engine
│   ├── metrics.py          # Prometheus metrics collector
│   └── streamer.py         # WebSocket telemetry broadcaster
├── kyber_pqc_kem/          # ML-KEM / CRYSTALS-Kyber engine
│   ├── agents.py           # PQC coordination agents
│   ├── cli.py              # CLI interface
│   ├── engine.py           # Core algorithmic engine
│   ├── models.py           # Data models
│   └── server.py           # FastAPI server factory
├── tests/                  # Test suite
├── web/                    # Operations console (HTML)
├── cli.py                  # Main CLI entry point
├── simulator.py            # High-throughput simulation
├── enrichment.py           # Enrichment feature suite
├── pyproject.toml          # Project configuration
├── Dockerfile              # Container build
├── docker-compose.yml      # Container orchestration
└── .github/workflows/      # CI/CD pipeline
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
