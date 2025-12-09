from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.call import CallLogResponse
from app.models.call_log import CallLog, CallStatus
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/calls", tags=["Calls"])


@router.get("/", response_model=List[CallLogResponse])
def get_call_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    bill_id: Optional[int] = None,
    status: Optional[CallStatus] = None,
    db: Session = Depends(get_db)
):
    """Get call logs with optional filtering"""
    try:
        query = db.query(CallLog)
        
        if bill_id:
            query = query.filter(CallLog.bill_id == bill_id)
        
        if status:
            query = query.filter(CallLog.status == status)
        
        call_logs = query.order_by(CallLog.created_at.desc()).offset(skip).limit(limit).all()
        
        return call_logs
        
    except Exception as e:
        logger.error(f"Error fetching call logs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{call_log_id}", response_model=CallLogResponse)
def get_call_log(call_log_id: int, db: Session = Depends(get_db)):
    """Get specific call log by ID"""
    call_log = db.query(CallLog).filter(CallLog.id == call_log_id).first()
    
    if not call_log:
        raise HTTPException(status_code=404, detail="Call log not found")
    
    return call_log


@router.get("/vapi/{vapi_call_id}", response_model=CallLogResponse)
def get_call_log_by_vapi_id(vapi_call_id: str, db: Session = Depends(get_db)):
    """Get call log by VAPI call ID"""
    call_log = db.query(CallLog).filter(CallLog.vapi_call_id == vapi_call_id).first()
    
    if not call_log:
        raise HTTPException(status_code=404, detail="Call log not found")
    
    return call_log
