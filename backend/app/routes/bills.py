from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.bill import BillCreate, BillUpdate, BillResponse, BillListResponse
from app.schemas.call import VapiCallRequest
from app.services.bill_service import BillService
from app.services.vapi_service import VapiService
from app.models.bill import BillStatus, Bill
from app.models.call_log import CallLog, CallStatus
from typing import Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/bills", tags=["Bills"])

vapi_service = VapiService()


@router.post("/", response_model=BillResponse)
def create_bill(bill: BillCreate, db: Session = Depends(get_db)):
    """Create a new bill"""
    try:
        # Check if bill already exists
        existing = BillService.get_bill_by_number(db, bill.bill_number)
        if existing:
            raise HTTPException(status_code=400, detail="Bill number already exists")
        
        new_bill = BillService.create_bill(db, bill)
        return new_bill
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating bill: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=BillListResponse)
def get_bills(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[BillStatus] = None,
    db: Session = Depends(get_db)
):
    """Get list of bills with optional filtering"""
    try:
        bills = BillService.get_bills(db, skip=skip, limit=limit, status=status)
        total = db.query(Bill).count()
        
        return BillListResponse(total=total, bills=bills)
        
    except Exception as e:
        logger.error(f"Error fetching bills: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{bill_id}", response_model=BillResponse)
def get_bill(bill_id: int, db: Session = Depends(get_db)):
    """Get bill by ID"""
    bill = BillService.get_bill(db, bill_id)
    
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    return bill


@router.put("/{bill_id}", response_model=BillResponse)
def update_bill(bill_id: int, bill_update: BillUpdate, db: Session = Depends(get_db)):
    """Update bill information"""
    bill = BillService.update_bill(db, bill_id, bill_update)
    
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    return bill


@router.delete("/{bill_id}")
def delete_bill(bill_id: int, db: Session = Depends(get_db)):
    """Delete a bill"""
    success = BillService.delete_bill(db, bill_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    return {"message": "Bill deleted successfully"}


@router.post("/{bill_id}/call")
async def initiate_call(bill_id: int, db: Session = Depends(get_db)):
    """Initiate a call for a specific bill"""
    try:
        bill = BillService.get_bill(db, bill_id)
        
        if not bill:
            raise HTTPException(status_code=404, detail="Bill not found")
        
        if bill.status == BillStatus.PAID:
            raise HTTPException(status_code=400, detail="Bill already paid")
        
        # Format date with ordinal suffix (1st, 2nd, 3rd, etc.)
        def get_ordinal_suffix(day):
            if 10 <= day % 100 <= 20:
                suffix = 'th'
            else:
                suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
            return suffix
        
        day = bill.due_date.day
        ordinal_day = f"{day}{get_ordinal_suffix(day)}"
        formatted_date = bill.due_date.strftime(f"{ordinal_day} %B %Y")
        
        # Prepare bill data for VAPI
        bill_data = {
            "customer_name": bill.customer_name,
            "bill_amount": bill.bill_amount,
            "due_date": formatted_date,  # e.g., "1st June 2025"
            "consumer_number": bill.consumer_number,
            "bill_number": bill.bill_number,
            "payment_link": bill.payment_link
        }
        
        # Initiate call via VAPI
        call_response = await vapi_service.initiate_call(
            phone_number=bill.customer_phone,
            bill_data=bill_data
        )
        
        # Create call log
        call_log = CallLog(
            bill_id=bill.id,
            vapi_call_id=call_response.get("id"),
            customer_phone=bill.customer_phone,
            status=CallStatus.INITIATED
        )
        
        db.add(call_log)
        db.commit()
        
        logger.info(f"Call initiated for bill {bill.bill_number}, Call ID: {call_response.get('id')}")
        
        return {
            "message": "Call initiated successfully",
            "call_id": call_response.get("id"),
            "bill_id": bill.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error initiating call: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pending/list")
def get_pending_bills(db: Session = Depends(get_db)):
    """Get all pending bills that need to be called"""
    try:
        bills = BillService.get_pending_bills(db)
        return {"total": len(bills), "bills": bills}
        
    except Exception as e:
        logger.error(f"Error fetching pending bills: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/overdue/list")
def get_overdue_bills(db: Session = Depends(get_db)):
    """Get all overdue bills"""
    try:
        bills = BillService.get_overdue_bills(db)
        return {"total": len(bills), "bills": bills}
        
    except Exception as e:
        logger.error(f"Error fetching overdue bills: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
