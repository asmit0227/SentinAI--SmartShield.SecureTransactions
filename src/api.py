from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.predictor import predict_transaction
from src.db_models import TransactionRecord
from src.database import get_db
from src.kafka_producer import send_transaction  
from datetime import datetime,timezone
from sqlalchemy import text
from src.database import engine
from confluent_kafka.admin import AdminClient
from src.redis import redis_client
from src.settings import KAFKA_BOOTSTRAP_SERVERS
from src.logger import get_logger

logger = get_logger(__name__)


kafka_admin=AdminClient({
      "bootstrap.servers":KAFKA_BOOTSTRAP_SERVERS
})


app=FastAPI(
    title="Real Time Fraud Detection API",
    version="1.0.0"
)
class Transaction(BaseModel):
    Time: float
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float
    Amount: float
class stream_transaction(Transaction):
      transaction_id:str  
      card_id:str  
class ReviewRequest(BaseModel):
    verdict: str      

@app.get("/")
def home():
        return {
        "message": "You Are Running Fraud Detection Api "
        }
@app.post("/predict")
def predict(transaction: Transaction,db:Session=Depends(get_db)):
        result= predict_transaction(transaction.model_dump())

        #database record
        add_record=TransactionRecord(
               amount=transaction.Amount,
              transaction_time=transaction.Time,

               prediction=result["prediction"],
               label=result["label"],
               fraud_probability=result["fraud_probability"],
               risk_level=result["risk_level"]
        )
        db.add(add_record)
        db.commit()

        db.refresh(add_record)

        

        return {
               **result ,
               "transaction_id":add_record.id
               }
      
def add_record_to_dict(record):
       return{
        "transaction_id": record.id,
        "external_transaction_id": record.external_transaction_id,
        "card_id": record.card_id,
        "amount": record.amount,
        "transaction_time": record.transaction_time,
        "prediction": record.prediction,
        "label": record.label,
        "fraud_probability": record.fraud_probability,
        "velocity_count": record.velocity_count,
        "risk_level": record.risk_level,
        "risk_reason":record.risk_reason,
        "decision":record.decision,
        "created_at": record.created_at,
        "review_status": record.review_status,
        "analyst_verdict": record.analyst_verdict,
        "reviewed_at": record.reviewed_at,
       }


def add_record_to_review(record):
       return{
        "transaction_id": record.id,
        "external_transaction_id": record.external_transaction_id,
        "card_id": record.card_id,
        "amount": record.amount,
        "label": record.label,
        "fraud_probability": record.fraud_probability,
        "velocity_count": record.velocity_count,
       
        "decision":record.decision,
        "created_at": record.created_at,
        "review_status": record.review_status,
        "analyst_verdict": record.analyst_verdict,
        "reviewed_at": record.reviewed_at,
       }
@app.get("/transactions")
def get_transactions(
       limit:int=50,
       db:Session=Depends(get_db)
):
       records=(db.query(TransactionRecord).order_by(TransactionRecord.id.desc()).limit(limit).all())

       return   [add_record_to_dict(record) for record in records]
           
       
@app.get("/transactions{transaction_id}")
def get_transaction(
       transaction_id=int,
       db:Session=Depends(get_db)
):
    
    record=db.query(TransactionRecord.id==transaction_id.first())

    if record is None:
          raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )
    else:
          return add_record_to_dict(record)

@app.get("/fraud/alerts")
def fraud_alerts(
      limit:int=100,
      db:Session=Depends(get_db)
)  :
      record=(db.query(TransactionRecord).filter(TransactionRecord.prediction==1 and TransactionRecord.decision == "review").order_by(TransactionRecord.id.desc()).limit(limit).all())

      return[add_record_to_dict(record) for record in record]

@app.get("/fraud/alert/review")
def fraud_alert_reviewed(
      limit:int=100,
      db:Session=Depends(get_db)
)  :
      record=(db.query(TransactionRecord).filter( TransactionRecord.decision == "review").order_by(TransactionRecord.id.desc()).limit(limit).all())

      return[add_record_to_review(record) for record in record]


@app.get("/analytics/summary")
def summary_dashboard(
      db:Session=Depends(get_db)
):
      total_transactions=db.query(func.count(TransactionRecord.id)).scalar()
      total_fraud_transactions=db.query(func.count(TransactionRecord.id)).filter(TransactionRecord.prediction==1).scalar()

      genuine_transactions=total_transactions-total_fraud_transactions

      avg_fraud_probability=(db.query(func.avg(TransactionRecord.fraud_probability)).scalar())
      fraud_rate=(
            (total_fraud_transactions/total_transactions)*100

            if total_transactions>0
            else print("No Transaction Data found")

      )
      return {
            "total_transaction":total_transactions,
            "total_fraud_transaction":total_fraud_transactions,
            "genuine_transaction":genuine_transactions,
            "average_fraud_probability":round(float(avg_fraud_probability or 0),6),
            "fraud_rate_percent":round(fraud_rate,4)
      }


@app.post(
    "/transactions/stream",
    status_code=202
)
def stream_transaction(transaction: stream_transaction):

    transaction_data = transaction.model_dump()

    try:
        send_transaction(transaction_data)

    except Exception:
        logger.exception(
            f"Kafka publish failed for transaction: "
            f"{transaction.transaction_id}"
        )

        raise HTTPException(
            status_code=503,
            detail="Transaction processing service is temporarily unavailable"
        )

    return {
        "status": "accepted",
        "transaction_id": transaction.transaction_id,
        "message": "Transaction accepted for processing"
    }
@app.get("/review/queue")
def review_queue(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    review_transactions = (
        db.query(TransactionRecord)
        .filter(
            TransactionRecord.decision == "review",
            TransactionRecord.review_status == "pending"
        )
        .order_by(TransactionRecord.id.desc())
        .limit(limit)
        .all()
    )

    return [
        add_record_to_dict(record)
        for record in review_transactions
    ]

@app.post("/review/{transaction_id}")
def resolve_review(
    transaction_id: int,
    review: ReviewRequest,
    db: Session = Depends(get_db)
):

    allowed_verdicts = [
        "confirmed_fraud",
        "legitimate"
    ]

    if review.verdict not in allowed_verdicts:
        raise HTTPException(
            status_code=400,
            detail="Verdict must be 'confirmed_fraud' or 'legitimate'"
        )


    transaction = (
        db.query(TransactionRecord)
        .filter(TransactionRecord.id == transaction_id)
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )


    if transaction.decision != "review":
        raise HTTPException(
            status_code=400,
            detail="Transaction is not in manual review"
        )

    
    if transaction.review_status == "resolved":
        raise HTTPException(
        status_code=409,
        detail="Transaction review is already resolved"
    )


    transaction.review_status = "resolved"
    transaction.analyst_verdict = review.verdict
    transaction.reviewed_at=datetime.now(timezone.utc)

    db.commit()
    db.refresh(transaction)


    return {
        "transaction_id": transaction.id,
        "review_status": transaction.review_status,
        "analyst_verdict": transaction.analyst_verdict,
        "reviewed_at":transaction.reviewed_at,
        "message": "Transaction review completed"
    }

@app.get("/health")
def health_check():

    services = {
        "api": "healthy"
    }

    # PostgreSQL
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.scalar()

        services["postgresql"] = "healthy"

    except Exception as error:
        print(f"PostgreSQL health check error: {error}")
        services["postgresql"] = "unhealthy"


    # Kafka
    try:
        kafka_admin.list_topics(timeout=3)

        services["kafka"] = "healthy"

    except Exception as error:
        print(f"Kafka health check error: {error}")
        services["kafka"] = "unhealthy"


    # Redis
    try:
        redis_client.ping()

        services["redis"] = "healthy"

    except Exception as error:
        print(f"Redis health check error: {error}")
        services["redis"] = "unhealthy"


    overall_status = (
        "healthy"
        if all(
            status == "healthy"
            for status in services.values()
        )
        else "degraded"
    )


    return {
        "status": overall_status,
        "services": services
    }
      



       

       