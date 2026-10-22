from src.predictor import predict_transaction


def test_genuine_transaction():

    transaction = {
        "Time": 8090.0,
        **{f"V{i}": 0.0 for i in range(1, 29)},
        "Amount": 0.0
    }

    result = predict_transaction(transaction)

    assert result["prediction"] == 0
    assert result["label"] == "genuine"
    assert result["fraud_probability"] < result["threshold"]


def test_fraud_transaction():

    transaction = {
        "Time": 8090.0,
        "V1": -1.78322883722709,
        "V2": 3.40279371307631,
        "V3": -3.82274226552205,
        "V4": 2.62536815276644,
        "V5": -1.97641541136284,
        "V6": -2.73168901231308,
        "V7": -3.43055914949085,
        "V8": 1.41320351399318,
        "V9": -0.776941494554916,
        "V10": -6.19988176274188,
        "V11": 4.36671348631445,
        "V12": -8.24326243368313,
        "V13": 0.345761165232579,
        "V14": -6.59055029705192,
        "V15": 0.265576095932165,
        "V16": -3.02845238846152,
        "V17": -4.21448627485607,
        "V18": -1.21360784773725,
        "V19": -0.265421595374812,
        "V20": 0.364089115014408,
        "V21": 0.454031931736316,
        "V22": -0.577525824201459,
        "V23": 0.0459665375362652,
        "V24": 0.461700017592254,
        "V25": 0.044146161217817,
        "V26": 0.305704433918549,
        "V27": 0.530980986346765,
        "V28": 0.243745598122111,
        "Amount": 1.0
    }

    result = predict_transaction(transaction)

    assert result["prediction"] == 1
    assert result["label"] == "fraud"
    assert result["fraud_probability"] >= result["threshold"]
    assert result["risk_level"] == "critical"