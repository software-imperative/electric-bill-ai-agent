from sqlalchemy.orm import Session
from app.models.payment import Payment, PaymentStatus, PaymentMethod
from app.schemas.payment import PaymentCreate, PaymentUpdate
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class PaymentService:
    """Service for payment processing operations"""
    
    @staticmethod
    def create_payment(db: Session, payment_data: PaymentCreate) -> Payment:
        """Create a new payment record"""
        payment = Payment(**payment_data.model_dump())
        
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment
    
    @staticmethod
    def get_payment(db: Session, payment_id: str) -> Optional[Payment]:
        """Get payment by payment ID"""
        return db.query(Payment).filter(Payment.payment_id == payment_id).first()
    
    @staticmethod
    def get_payment_by_bill(db: Session, bill_id: int) -> Optional[Payment]:
        """Get payment for a specific bill"""
        return db.query(Payment).filter(Payment.bill_id == bill_id).first()
    
    @staticmethod
    def update_payment(
        db: Session,
        payment_id: str,
        payment_update: PaymentUpdate
    ) -> Optional[Payment]:
        """Update payment information"""
        payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
        
        if not payment:
            return None
        
        update_data = payment_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(payment, field, value)
        
        db.commit()
        db.refresh(payment)
        return payment
    
    @staticmethod
    def mark_payment_completed(
        db: Session,
        payment_id: str,
        transaction_id: str,
        payment_method: Optional[PaymentMethod] = None
    ) -> Optional[Payment]:
        """Mark payment as completed"""
        payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
        
        if not payment:
            logger.error(f"Payment not found: {payment_id}")
            return None
        
        payment.status = PaymentStatus.COMPLETED
        payment.transaction_id = transaction_id
        payment.payment_date = datetime.utcnow()
        
        if payment_method:
            payment.payment_method = payment_method
        
        db.commit()
        db.refresh(payment)
        
        logger.info(f"Payment completed: {payment_id}, Transaction: {transaction_id}")
        return payment
    
    @staticmethod
    def mark_payment_failed(
        db: Session,
        payment_id: str,
        error_message: str
    ) -> Optional[Payment]:
        """Mark payment as failed"""
        payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
        
        if not payment:
            return None
        
        payment.status = PaymentStatus.FAILED
        payment.error_message = error_message
        
        db.commit()
        db.refresh(payment)
        
        logger.warning(f"Payment failed: {payment_id}, Error: {error_message}")
        return payment
    
    @staticmethod
    def process_payment_callback(
        db: Session,
        payment_id: str,
        transaction_id: str,
        status: str,
        payment_method: Optional[str] = None,
        gateway_response: Optional[str] = None
    ) -> Optional[Payment]:
        """Process payment gateway callback"""
        payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
        
        if not payment:
            logger.error(f"Payment not found for callback: {payment_id}")
            return None
        
        # Map gateway status to internal status
        status_mapping = {
            "success": PaymentStatus.COMPLETED,
            "completed": PaymentStatus.COMPLETED,
            "failed": PaymentStatus.FAILED,
            "pending": PaymentStatus.PROCESSING
        }
        
        payment.status = status_mapping.get(status.lower(), PaymentStatus.PROCESSING)
        payment.transaction_id = transaction_id
        payment.gateway_response = gateway_response
        
        if payment.status == PaymentStatus.COMPLETED:
            payment.payment_date = datetime.utcnow()
        
        if payment_method:
            try:
                payment.payment_method = PaymentMethod(payment_method.lower())
            except ValueError:
                payment.payment_method = PaymentMethod.OTHER
        
        db.commit()
        db.refresh(payment)
        
        logger.info(f"Payment callback processed: {payment_id}, Status: {payment.status}")
        return payment
