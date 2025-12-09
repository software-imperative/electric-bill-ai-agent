from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.call_log import CallStatus, CallOutcome


class CallLogBase(BaseModel):
    bill_id: int
    customer_phone: str


class CallLogCreate(CallLogBase):
    vapi_call_id: Optional[str] = None


class CallLogUpdate(BaseModel):
    status: Optional[CallStatus] = None
    outcome: Optional[CallOutcome] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    duration: Optional[int] = None
    transcript: Optional[str] = None
    recording_url: Optional[str] = None
    sms_sent: Optional[bool] = None
    sms_sid: Optional[str] = None
    error_message: Optional[str] = None


class CallLogResponse(CallLogBase):
    id: int
    vapi_call_id: Optional[str] = None
    status: CallStatus
    outcome: Optional[CallOutcome] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    duration: Optional[int] = None
    transcript: Optional[str] = None
    recording_url: Optional[str] = None
    sms_sent: int
    sms_sid: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class VapiWebhookEvent(BaseModel):
    """VAPI webhook event payload"""
    message: dict
    call: Optional[dict] = None
    phoneNumber: Optional[dict] = None
    customer: Optional[dict] = None
    artifact: Optional[dict] = None
    timestamp: Optional[str] = None


class VapiCallRequest(BaseModel):
    """Request to initiate a call via VAPI"""
    phone_number: str
    bill_id: int
    assistant_id: Optional[str] = None
