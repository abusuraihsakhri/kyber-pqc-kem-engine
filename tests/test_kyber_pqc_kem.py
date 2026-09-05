import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from kyber_pqc_kem.models import FrontierPayload, ExecutionStatus
from kyber_pqc_kem.engine import FrontierDomainEngine
from kyber_pqc_kem.agents import LatticePolynomialAgent, NTTVectorTransformAgent, DecapsulationIntegrityAgent, PQCKeyAgreementCoordinator
from kyber_pqc_kem.cli import main, _safe_resolve_path


def test_sub_agents():
    a1 = LatticePolynomialAgent()
    p1 = FrontierPayload("T1", "KEY-01", primary_metric=35.0, secondary_metric=4.0, status_descriptor="NOMINAL")
    alerts1 = a1.audit(p1)
    assert len(alerts1) == 1
    assert alerts1[0].status == ExecutionStatus.ELEVATED_RISK

    a2 = NTTVectorTransformAgent()
    p2 = FrontierPayload("T2", "KEY-02", primary_metric=10.0, secondary_metric=15.0, status_descriptor="NOMINAL", is_critical_flag=True)
    alerts2 = a2.audit(p2)
    assert len(alerts2) == 1
    assert alerts2[0].status == ExecutionStatus.CRITICAL_INTERVENTION

    a3 = DecapsulationIntegrityAgent()
    p3 = FrontierPayload("T3", "KEY-03", primary_metric=10.0, secondary_metric=4.0, status_descriptor="DISCORDANT_ANOMALY")
    alerts3 = a3.audit(p3)
    assert len(alerts3) == 1


def test_coordinator():
    coord = PQCKeyAgreementCoordinator()
    p_nominal = FrontierPayload("T4", "KEY-04", primary_metric=12.0, secondary_metric=4.0, status_descriptor="NOMINAL")
    dossier = coord.process(p_nominal)
    assert dossier["overall_status"] == ExecutionStatus.NOMINAL.value
    assert dossier["total_alerts"] == 0

    ans = coord.query_supervisory_chat("What standard is applied?")
    assert "NIST FIPS 203 (ML-KEM Standard)" in ans or "specifications" in ans


def test_cli():
    assert main(["audit", "--task-id", "CLI-01"]) == 0
    assert main(["chat", "What", "is", "the", "system", "status?"]) == 0


def test_safe_path_resolution():
    """Test that path resolution validates file existence."""
    # Existing file should resolve
    existing = _safe_resolve_path("sample.csv", must_exist=True)
    assert existing.exists()

    # Non-existing file with must_exist=True should raise
    with pytest.raises(Exception):
        _safe_resolve_path("nonexistent_file_xyz.csv", must_exist=True)

    # Non-existing file with must_exist=False should resolve
    non_existing = _safe_resolve_path("output_results.csv", must_exist=False)
    assert not non_existing.exists()
