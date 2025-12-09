from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.bill import BillStatus


class BillBase(BaseModel):
    customer_name: str
    customer_phone: str
    customer_email: Optional[str] = None
    consumer_number: str
    bill_number: str
    bill_amount: float
    due_date: datetime
    billing_period: Optional[str] = None


class BillCreate(BillBase):
    pass


class BillUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    bill_amount: Optional[float] = None
    due_date: Optional[datetime] = None
    status: Optional[BillStatus] = None
    notes: Optional[str] = None


class BillResponse(BillBase):
    id: int
    status: BillStatus
    payment_link: Optional[str] = None
    payment_id: Optional[str] = None
    payment_date: Optional[datetime] = None
    call_attempts: int
    last_call_date: Optional[datetime] = None
    next_reminder_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True


class BillListResponse(BaseModel):
    total: int
    bills: list[BillResponse]
