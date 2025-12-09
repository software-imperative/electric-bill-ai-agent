from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.payment import PaymentStatus, PaymentMethod


class PaymentBase(BaseModel):
    bill_id: int
    amount: float


class PaymentCreate(PaymentBase):
    payment_id: str
    payment_method: Optional[PaymentMethod] = None


class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatus] = None
    transaction_id: Optional[str] = None
    payment_method: Optional[PaymentMethod] = None
    payment_date: Optional[datetime] = None
    gateway_response: Optional[str] = None
    error_message: Optional[str] = None


class PaymentResponse(PaymentBase):
    id: int
    payment_id: str
    transaction_id: Optional[str] = None
    payment_method: Optional[PaymentMethod] = None
    status: PaymentStatus
    payment_date: Optional[datetime] = None
    gateway_response: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PaymentCallbackRequest(BaseModel):
    """Payment gateway callback payload"""
    payment_id: str
    transaction_id: str
    status: str
    amount: float
    payment_method: Optional[str] = None
    gateway_response: Optional[dict] = None
