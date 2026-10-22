import json
import joblib
from pathlib import Path
import pandas as pd

BASE_DIR=Path(__file__).resolve().parent.parent
MODEL_DIR= BASE_DIR/"models"

MODEL_PATH=MODEL_DIR/"xgb_fraud_model.pkl"
FEATURE_PATH=MODEL_DIR/"feature_order.json"
METADATA=MODEL_DIR/"model_metadata.json"

model =joblib.load(MODEL_PATH)

with open(
  FEATURE_PATH, "r"  
) as f:
    features_list=json.load(f)

with open(
  METADATA, "r"  
) as f:
    metadatas=json.load(f)    

model_threshold=metadatas["threshold"]    


def predict_transaction(transaction : dict):
    transaction_df= pd.DataFrame([transaction])
    transaction_df=transaction_df[features_list]

    transaction_proba=model.predict_proba(transaction_df)[:,1][0]

    prediction=int(transaction_proba>=model_threshold)

    label="fraud" if prediction==1 else "genuine" 

    if transaction_proba<0.10:
        risk_level="low"
    elif transaction_proba<0.30:
        risk_level="medium"
    elif transaction_proba<0.60:
        risk_level="high"   
    else:
        risk_level="critical"     
    return {

      "prediction":prediction,
      "label":label,
      "fraud_probability":float(transaction_proba),
       "fraud_probability_percent": round(
                  float(transaction_proba) * 100,
                  4),
      "risk_level" : risk_level , 
      "threshold":float(model_threshold)
      
          
    }