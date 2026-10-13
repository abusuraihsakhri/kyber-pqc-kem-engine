"""Regression tests for CSV parsing, parameter validation, and demo boundaries."""
import csv
from pathlib import Path

import pytest
from pydantic import ValidationError

from cli import main, parse_csv_bool
from kyber_pqc_kem.cli import parse_csv_bool as legacy_parse_csv_bool
from agents.base import AuditTrail
from agents.llm_factory import LLMFactory
from agents.models import SystemTaskPayload
from kyber_pqc_kem.models import FrontierPayload


@pytest.mark.parametrize("value,expected", [
    ("false", False), ("False", False), ("0", False), ("no", False),
    ("", False), ("true", True), ("TRUE", True), ("1", True),
    ("yes", True), ("on", True),
])
def test_csv_boolean_parsing(value, expected):
    assert parse_csv_bool(value) is expected
    assert legacy_parse_csv_bool(value) is expected


def test_csv_boolean_rejects_invalid_value():
    with pytest.raises(ValueError, match="Invalid is_critical_flag"):
        parse_csv_bool("perhaps")


def test_false_csv_value_does_not_escalate(tmp_path):
    source = tmp_path / "input.csv"
    target = tmp_path / "output.csv"
    with source.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=[
            "task_id", "target_identifier", "primary_metric",
            "secondary_metric", "status_descriptor", "is_critical_flag"
        ])
        writer.writeheader()
        writer.writerow(dict(task_id="TEST", target_identifier="KEY-01",
                             primary_metric=4, secondary_metric=2,
                             status_descriptor="NOMINAL", is_critical_flag="False"))
    assert main(["batch", "-i", str(source), "-o", str(target)]) == 0
    with target.open(newline="", encoding="utf-8") as fh:
        row = next(csv.DictReader(fh))
    assert row["overall_urgency"] == "ROUTINE"
    assert row["total_alerts"] == "0"
    with pytest.raises(ValueError, match="must differ"):
        main(["batch", "-i", str(source), "-o", str(source)])
    assert source.exists()


@pytest.mark.parametrize("metric", [float("nan"), float("inf"), float("-inf")])
def test_nonfinite_values_rejected(metric):
    with pytest.raises(ValidationError):
        SystemTaskPayload(task_id="TASK", target_identifier="KEY", primary_metric=metric)
    with pytest.raises(ValueError):
        FrontierPayload(task_id="TASK", target_identifier="KEY", primary_metric=metric,
                        secondary_metric=1, status_descriptor="NOMINAL")


def test_llm_provider_is_not_silently_mocked():
    assert "No cryptographic validation" in LLMFactory.create("mock").invoke("status")
    for unsupported in ("openai", "claude", "ollama", "other"):
        with pytest.raises(ValueError, match="only mock"):
            LLMFactory.create(unsupported)


def test_audit_trail_readout_is_snapshot():
    trail = AuditTrail("test-key")
    trail.log("actor", "role", "event", {"value": 3})
    view = trail.get_trail()
    view[0]["payload_hash"] = "modified"
    assert trail.verify_integrity()
    assert view[0]["payload_hash"] != trail.get_trail()[0]["payload_hash"]


def test_api_rejects_nonfinite_metrics():
    from fastapi.testclient import TestClient
    from agents.api import app
    client = TestClient(app)
    result = client.post("/api/audit", json={
        "task_id": "t", "target_identifier": "key",
        "primary_metric": 1e309,
    })
    assert result.status_code == 422


def test_audit_trail_rejects_missing_or_ambiguous_fields():
    trail = AuditTrail("test-key")
    trail.log("a|b", "tier", "event", {"value": 3})
    trail.logs[0]["actor"] = "a"
    trail.logs[0]["actor_tier"] = "b|tier"
    assert not trail.verify_integrity()
    trail.logs[0].pop("actor_tier")
    assert not trail.verify_integrity()


def test_simulator_rejects_zero_iterations():
    from simulator import run_simulation
    with pytest.raises(ValueError, match="positive"):
        run_simulation(0)
