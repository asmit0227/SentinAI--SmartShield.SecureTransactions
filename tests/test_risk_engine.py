from src.risk_engine import calculate_risk


def test_low_risk():
    assert calculate_risk(0.01, 1) == "low"


def test_medium_velocity():
    assert calculate_risk(0.01, 5) == "medium"


def test_high_velocity():
    assert calculate_risk(0.01, 7) == "high"


def test_critical_velocity():
    assert calculate_risk(0.01, 10) == "critical"


def test_critical_ml_probability():
    assert calculate_risk(0.95, 1) == "critical"

