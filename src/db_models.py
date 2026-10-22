from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func

from src.database import Base


class TransactionRecord(Base):
    __tablename__ = "transactions"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    external_transaction_id=Column(
            String,
            index=True,
            unique=True,
            nullable=True
        )

    card_id = Column(
        String, 
        nullable=True, 
        index=True)

    

    amount = Column(
        Float,
        nullable=False
    )

    transaction_time = Column(
        Float,
        nullable=False
    )

    prediction = Column(
        Integer,
        nullable=False
    )

    label = Column(
        String,
        nullable=False
    )

    fraud_probability = Column(
        Float,
        nullable=False
    )
    velocity_count = Column(
        Integer, nullable=True)

    risk_reason = Column(
        String, nullable=True)

    decision = Column(
        String, 
        nullable=True)

    review_status=Column(
        String,
        nullable=True

    )

    analyst_verdict = Column(
        String,
        nullable=True)

    reviewed_at=Column(
        DateTime(timezone=True,),nullable=True
    )

    
    risk_level = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )