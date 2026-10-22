def calculate_risk(
        fraud_rate:float,
        velocity_count:int
):
    if fraud_rate>=0.60:
        risk_level="critical"
    elif fraud_rate>=0.30:
        risk_level="high"
    elif fraud_rate>=0.10:
        risk_level="medium"
    else:
        risk_level="low"

    if velocity_count>=10:
        risk_level="critical"
    if  velocity_count>=7 and risk_level in ["low" , "medium"]:
        risk_level="high"
    if velocity_count>=5 and risk_level=="low":
        risk_level="medium"

    return risk_level    

def get_risk_reason(
    fraud_rate: float,
    velocity_count: int
):

    reasons = []

    if fraud_rate >= 0.60:
        reasons.append("Very high ML fraud probability")

    elif fraud_rate >= 0.30:
        reasons.append("High ML fraud probability")

    elif fraud_rate >= 0.10:
        reasons.append("Elevated ML fraud probability")

        


    if velocity_count >= 10:
        reasons.append(
            f"Extreme transaction velocity: "
            f"{velocity_count} transactions in last 5 minutes"
        )

    elif velocity_count >= 7:
        reasons.append(
            f"High transaction velocity: "
            f"{velocity_count} transactions in last 5 minutes"
        )

    elif velocity_count >= 5:
        reasons.append(
            f"Elevated transaction velocity: "
            f"{velocity_count} transactions in last 5 minutes"
        )


    if not reasons:
        return "No significant risk indicators"


    return " | ".join(reasons)