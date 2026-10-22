from src.decision_engine import get_transaction_decision


def test_low_risk_approve():
    assert get_transaction_decision("low") == "approve"


def test_medium_risk_review():
    assert get_transaction_decision("medium") == "review"


def test_high_risk_review():
    assert get_transaction_decision("high") == "review"


def test_critical_risk_block():
    assert get_transaction_decision("critical") == "block"    