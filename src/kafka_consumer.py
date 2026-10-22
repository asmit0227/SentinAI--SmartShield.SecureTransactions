import json
from confluent_kafka import Consumer, Producer
from src.risk_engine import calculate_risk,get_risk_reason
from src.predictor import predict_transaction,features_list
from src.database import SessionLocal
from src.db_models import TransactionRecord
from src.redis_features import record_transaction_velocity
from src.decision_engine import get_transaction_decision
from src.settings import KAFKA_BOOTSTRAP_SERVERS
from src.logger import get_logger

logger=get_logger(__name__)




# 1. KAFKA SETTINGS



TOPIC = "fraud-transactions"
DLQ_TOPIC = "fraud-dead-letter"



# 2. MAIN CONSUMER


consumer = Consumer({
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "group.id": "fraud-detection-services",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False
})



# 3. DLQ PRODUCER


dlq_producer = Producer({
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS
})



# 4. DLQ HELPER FUNCTION


def send_to_dlq(message, payload, error):

    dlq_message = {
        "original_payload": payload,
        "error": str(error),
        "source_topic": message.topic(),
        "partition": message.partition(),
        "offset": message.offset()
    }

    dlq_producer.produce(
        topic=DLQ_TOPIC,
        value=json.dumps(dlq_message)
    )

    remaining_messages = dlq_producer.flush()

    return remaining_messages == 0



# 5. SUBSCRIBE MAIN TOPIC


consumer.subscribe([TOPIC])

logger.info("Consumer started")
logger.info("Waiting for transactions")



# 6. CONSUMER LOOP


try:

    while True:

        message = consumer.poll(1.0)

        if message is None:
            continue

        if message.error():
            logger.error(f"Unexpected Kafka Error: {message.error()}")
            continue


       

        db = None
        transaction = None

        raw_payload = message.value().decode(
            "utf-8",
            errors="replace"
        )


        try:

         
            # 7. JSON CONVERSION
          

            transaction = json.loads(raw_payload)

            logger.info(
                       f"Transaction_id: "
                       f"{transaction.get('transaction_id')} | "
                       f"cardid={transaction.get('card_id')}"
                          )

          


          
            # 8. DATABASE SESSION
         

            db = SessionLocal()


         
            # 9. DUPLICATE CHECK
          

            ext_transaction_id = transaction.get(
                "transaction_id"
            )

            if not ext_transaction_id:
                raise ValueError(
                    "transaction_id is missing"
                )
            #CARD_ID

            card_id = transaction.get("card_id")

            if not card_id:
              raise ValueError("card_id is missing")


            check_record = (
                db.query(TransactionRecord)
                .filter(
                    TransactionRecord.external_transaction_id
                    == ext_transaction_id
                )
                .first()
            )


            if check_record:

                logger.warning(
                    f"Duplicate transaction skipped: "
                    f"{ext_transaction_id}"
                )

                consumer.commit(
                    message=message,
                    asynchronous=False
                )

                continue


            
            # 10.CHECKING FOR FEATURE IF ANY MISSING
            missing_features = [feature for feature in features_list if feature not in transaction]

            if missing_features:
             raise ValueError(f"Missing required features: {missing_features}")

            #REDIS FEATURE

            card_id=transaction.get("card_id")
            if not card_id:
                raise ValueError("card id is missing")


            velocity_count=record_transaction_velocity(
                card_id=card_id,
                transaction_id=ext_transaction_id
            )
            logger.info(f" velocity count for {card_id} is {velocity_count} in last 5 minutes ")


           
            # 11.MODEL PREDICTION
            result = predict_transaction(transaction)
            logger.info(
                        f"Fraud prediction: "
                        f"label={result['label']}, "
                        f"probability={result['fraud_probability']:.6f}"
                       )
            #FINAL RISK CALCULATE

            final_risk=calculate_risk(fraud_rate=result["fraud_probability"],
                                      velocity_count=velocity_count )
            
            logger.info(f"Fraud risk ML : {result["risk_level"]}")
            logger.info(f"Final risk : {final_risk}")

            #RISK REASON

            risk_reason = get_risk_reason(
                          fraud_rate=result["fraud_probability"],
                          velocity_count=velocity_count
            )
            logger.info(f"Risk reason : {risk_reason}")

            #DECISION_ENGINE

            decision=get_transaction_decision(final_risk)
            logger.info(f"Decision : {decision}")


            if not decision:
                raise ValueError("decision is not available")
            
            # 11. SAVE RESULT IN POSTGRESQL
            

            record = TransactionRecord(

                external_transaction_id=ext_transaction_id,

                amount=transaction["Amount"],
                transaction_time=transaction["Time"],

                prediction=result["prediction"],
                label=result["label"],

                fraud_probability=result[
                    "fraud_probability"
                ],
                velocity_count=velocity_count,
                card_id=card_id,
                risk_reason=risk_reason,
                decision=decision,
                review_status="pending" if decision=="review" else None,
                analyst_verdict=None,

                risk_level=final_risk
            )


            db.add(record)
            db.commit()
            db.refresh(record)


            logger.info(
                f"Record {record.id} successfully "
                f"saved in database"
            )


            
            # 12. SUCCESS → COMMIT KAFKA OFFSET
             

            consumer.commit(
                message=message,
                asynchronous=False
            )


        # 13. ANY PROCESSING FAILURE → DLQ
        

        except Exception as error:

            if db is not None:
                db.rollback()


            logger.exception(f"Transaction processing failed: {transaction}")


            # Agar JSON parse ho gaya tha
            # to dictionary save karenge.
            # Nahi hua to raw string save hogi.

            failed_payload = (
                transaction
                if transaction is not None
                else raw_payload
            )


            dlq_success = send_to_dlq(
                message=message,
                payload=failed_payload,
                error=error
            )


            if dlq_success:

                logger.warning(f"Failed transaction sent to DLQ: {ext_transaction_id}"
)


                # Original event ko handled mark karo
                consumer.commit(
                    message=message,
                    asynchronous=False
                )


            else:

                logger.warning(
                    "DLQ delivery failed. "
                    "Kafka offset NOT committed."
                )


        
        # 14. CLOSE DB SESSION

        finally:

            if db is not None:
                db.close()


except KeyboardInterrupt:

    print("\nConsumer stopped")


finally:

    consumer.close()