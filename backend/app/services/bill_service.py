from sqlalchemy.orm import Session
from app.models.bill import Bill, BillStatus
from app.schemas.bill import BillCreate, BillUpdate
from datetime import datetime, timedelta
from typing import List, Optional
from app.config import get_settings
import uuid

settings = get_settings()


class BillService:
    """Service for bill management operations"""
    
    @staticmethod
    def create_bill(db: Session, bill_data: BillCreate) -> Bill:
        """Create a new bill"""
        # Generate payment link
        payment_link = f"{settings.payment_gateway_url}/pay/{uuid.uuid4().hex}"
        
        bill = Bill(
            **bill_data.model_dump(),
            payment_link=payment_link,
            status=BillStatus.PENDING
        )
        
        db.add(bill)
        db.commit()
        db.refresh(bill)
        return bill
    
    @staticmethod
    def get_bill(db: Session, bill_id: int) -> Optional[Bill]:
        """Get bill by ID"""
        return db.query(Bill).filter(Bill.id == bill_id).first()
    
    @staticmethod
    def get_bill_by_number(db: Session, bill_number: str) -> Optional[Bill]:
        """Get bill by bill number"""
        return db.query(Bill).filter(Bill.bill_number == bill_number).first()
    
    @staticmethod
    def get_bills(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[BillStatus] = None
    ) -> List[Bill]:
        """Get list of bills with optional filtering"""
        query = db.query(Bill)
        
        if status:
            query = query.filter(Bill.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_bill(db: Session, bill_id: int, bill_update: BillUpdate) -> Optional[Bill]:
        """Update bill information"""
        bill = db.query(Bill).filter(Bill.id == bill_id).first()
        
        if not bill:
            return None
        
        update_data = bill_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(bill, field, value)
        
        db.commit()
        db.refresh(bill)
        return bill
    
    @staticmethod
    def mark_bill_called(db: Session, bill_id: int) -> Optional[Bill]:
        """Mark bill as called and increment call attempts"""
        bill = db.query(Bill).filter(Bill.id == bill_id).first()
        
        if not bill:
            return None
        
        bill.status = BillStatus.CALLED
        bill.call_attempts += 1
        bill.last_call_date = datetime.utcnow()
        
        # Set next reminder date
        bill.next_reminder_date = datetime.utcnow() + timedelta(
            hours=settings.reminder_interval_hours
        )
        
        db.commit()
        db.refresh(bill)
        return bill
    
    @staticmethod
    def mark_bill_paid(
        db: Session,
        bill_id: int,
        payment_id: str,
        payment_date: datetime
    ) -> Optional[Bill]:
        """Mark bill as paid"""
        bill = db.query(Bill).filter(Bill.id == bill_id).first()
        
        if not bill:
            return None
        
        bill.status = BillStatus.PAID
        bill.payment_id = payment_id
        bill.payment_date = payment_date
        
        db.commit()
        db.refresh(bill)
        return bill
    
    @staticmethod
    def get_pending_bills(db: Session) -> List[Bill]:
        """Get all pending bills that need to be called"""
        return db.query(Bill).filter(
            Bill.status.in_([BillStatus.PENDING, BillStatus.OVERDUE]),
            Bill.call_attempts < settings.call_retry_attempts
        ).all()
    
    @staticmethod
    def get_overdue_bills(db: Session) -> List[Bill]:
        """Get bills that are overdue"""
        now = datetime.utcnow()
        bills = db.query(Bill).filter(
            Bill.due_date < now,
            Bill.status != BillStatus.PAID
        ).all()
        
        # Update status to overdue
        for bill in bills:
            if bill.status != BillStatus.OVERDUE:
                bill.status = BillStatus.OVERDUE
        
        db.commit()
        return bills
    
    @staticmethod
    def delete_bill(db: Session, bill_id: int) -> bool:
        """Delete a bill"""
        bill = db.query(Bill).filter(Bill.id == bill_id).first()
        
        if not bill:
            return False
        
        db.delete(bill)
        db.commit()
        return True
