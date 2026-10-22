def get_transaction_decision(risk_level: str):

    risk_level = risk_level.lower()

    if risk_level == "critical":
        return "block"

    elif risk_level in ["medium", "high"]:
        return "review"

    else:
        return "approve"