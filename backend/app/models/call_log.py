from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.sql import func
from app.database import Base
import enum


class CallStatus(str, enum.Enum):
    INITIATED = "initiated"
    RINGING = "ringing"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    NO_ANSWER = "no_answer"
    BUSY = "busy"


class CallOutcome(str, enum.Enum):
    PAYMENT_CONFIRMED = "payment_confirmed"
    PAYMENT_PROMISED = "payment_promised"
    CUSTOMER_DISPUTED = "customer_disputed"
    NO_RESPONSE = "no_response"
    WRONG_NUMBER = "wrong_number"
    CALLBACK_REQUESTED = "callback_requested"


class CallLog(Base):
    __tablename__ = "call_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=False, index=True)
    
    vapi_call_id = Column(String, nullable=True, unique=True, index=True)
    customer_phone = Column(String, nullable=False)
    
    status = Column(SQLEnum(CallStatus), default=CallStatus.INITIATED, index=True)
    outcome = Column(SQLEnum(CallOutcome), nullable=True)
    
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    duration = Column(Integer, nullable=True)  # in seconds
    
    transcript = Column(Text, nullable=True)
    recording_url = Column(String, nullable=True)
    
    sms_sent = Column(Integer, default=0)
    sms_sid = Column(String, nullable=True)
    
    error_message = Column(String, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
