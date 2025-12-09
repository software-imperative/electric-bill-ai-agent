from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from app.database import Base
import enum


class BillStatus(str, enum.Enum):
    PENDING = "pending"
    CALLED = "called"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class Bill(Base):
    __tablename__ = "bills"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False, index=True)
    customer_email = Column(String, nullable=True)
    consumer_number = Column(String, nullable=False, unique=True, index=True)
    
    bill_number = Column(String, nullable=False, unique=True, index=True)
    bill_amount = Column(Float, nullable=False)
    due_date = Column(DateTime, nullable=False)
    billing_period = Column(String, nullable=True)
    
    status = Column(SQLEnum(BillStatus), default=BillStatus.PENDING, index=True)
    
    payment_link = Column(String, nullable=True)
    payment_id = Column(String, nullable=True)
    payment_date = Column(DateTime, nullable=True)
    
    call_attempts = Column(Integer, default=0)
    last_call_date = Column(DateTime, nullable=True)
    next_reminder_date = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    notes = Column(String, nullable=True)
