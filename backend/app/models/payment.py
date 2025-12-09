from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from app.database import Base
import enum


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentMethod(str, enum.Enum):
    UPI = "upi"
    CARD = "card"
    NET_BANKING = "net_banking"
    WALLET = "wallet"
    CASH = "cash"
    OTHER = "other"


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=False, index=True)
    
    payment_id = Column(String, nullable=False, unique=True, index=True)
    transaction_id = Column(String, nullable=True, index=True)
    
    amount = Column(Float, nullable=False)
    payment_method = Column(SQLEnum(PaymentMethod), nullable=True)
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, index=True)
    
    payment_date = Column(DateTime, nullable=True)
    
    gateway_response = Column(String, nullable=True)
    error_message = Column(String, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
