"""
Seed script to populate database with sample bill data
Run this script to create 10 sample bills with Indian customer data
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, init_db
from app.models.bill import Bill, BillStatus
import uuid


def generate_payment_link():
    """Generate a dummy payment link"""
    return f"https://payment.adani.com/pay/{uuid.uuid4().hex[:16]}"


def create_sample_bills():
    """Create 10 sample bills with Indian customer data"""
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    # Sample customer data with real Indian names
    customers = [
        {
            "customer_name": "Mayur Gadekar",
            "customer_phone": "+919975711324",
            "customer_email": "mayur.gadekar@gmail.com",
            "consumer_number": "CONS001",
            "bill_number": "BILL2024001",
            "bill_amount": 2450.50,
            "billing_period": "November 2024"
        },
        {
            "customer_name": "Rajesh Kumar Singh",
            "customer_phone": "+919876543210",
            "customer_email": "rajesh.singh@gmail.com",
            "consumer_number": "CONS002",
            "bill_number": "BILL2024002",
            "bill_amount": 3200.00,
            "billing_period": "November 2024"
        },
        {
            "customer_name": "Priya Sharma",
            "customer_phone": "+919823456789",
            "customer_email": "priya.sharma@yahoo.com",
            "consumer_number": "CONS003",
            "bill_number": "BILL2024003",
            "bill_amount": 1850.75,
            "billing_period": "November 2024"
        },
        {
            "customer_name": "Amit Patel",
            "customer_phone": "+919765432109",
            "customer_email": "amit.patel@gmail.com",
            "consumer_number": "CONS004",
            "bill_number": "BILL2024004",
            "bill_amount": 4100.25,
            "billing_period": "November 2024"
        },
        {
            "customer_name": "Sneha Deshmukh",
            "customer_phone": "+919912345678",
            "customer_email": "sneha.deshmukh@outlook.com",
            "consumer_number": "CONS005",
            "bill_number": "BILL2024005",
            "bill_amount": 2750.00,
            "billing_period": "November 2024"
        },
        {
            "customer_name": "Vikram Reddy",
            "customer_phone": "+919834567890",
            "customer_email": "vikram.reddy@gmail.com",
            "consumer_number": "CONS006",
            "bill_number": "BILL2024006",
            "bill_amount": 3650.50,
            "billing_period": "November 2024"
        },
        {
            "customer_name": "Anjali Verma",
            "customer_phone": "+919745678901",
            "customer_email": "anjali.verma@gmail.com",
            "consumer_number": "CONS007",
            "bill_number": "BILL2024007",
            "bill_amount": 1950.00,
            "billing_period": "November 2024"
        },
        {
            "customer_name": "Suresh Iyer",
            "customer_phone": "+919656789012",
            "customer_email": "suresh.iyer@yahoo.com",
            "consumer_number": "CONS008",
            "bill_number": "BILL2024008",
            "bill_amount": 5200.75,
            "billing_period": "November 2024"
        },
        {
            "customer_name": "Kavita Joshi",
            "customer_phone": "+919567890123",
            "customer_email": "kavita.joshi@gmail.com",
            "consumer_number": "CONS009",
            "bill_number": "BILL2024009",
            "bill_amount": 2100.00,
            "billing_period": "November 2024"
        },
        {
            "customer_name": "Arjun Nair",
            "customer_phone": "+919478901234",
            "customer_email": "arjun.nair@outlook.com",
            "consumer_number": "CONS010",
            "bill_number": "BILL2024010",
            "bill_amount": 3850.25,
            "billing_period": "November 2024"
        }
    ]
    
    # Create bills with varying due dates and statuses
    today = datetime.now()
    
    bills_created = 0
    
    for i, customer in enumerate(customers):
        # Vary the due dates
        if i < 3:
            # Overdue bills
            due_date = today - timedelta(days=random.randint(5, 15))
            status = BillStatus.OVERDUE
        elif i < 6:
            # Due soon (within next 7 days)
            due_date = today + timedelta(days=random.randint(1, 7))
            status = BillStatus.PENDING
        elif i < 8:
            # Already called
            due_date = today + timedelta(days=random.randint(8, 15))
            status = BillStatus.CALLED
        else:
            # Paid bills
            due_date = today + timedelta(days=random.randint(10, 20))
            status = BillStatus.PAID
        
        # Check if bill already exists
        existing_bill = db.query(Bill).filter(Bill.bill_number == customer["bill_number"]).first()
        
        if existing_bill:
            print(f"⚠️  Bill {customer['bill_number']} already exists for {customer['customer_name']}, skipping...")
            continue
        
        # Create bill
        bill = Bill(
            customer_name=customer["customer_name"],
            customer_phone=customer["customer_phone"],
            customer_email=customer["customer_email"],
            consumer_number=customer["consumer_number"],
            bill_number=customer["bill_number"],
            bill_amount=customer["bill_amount"],
            due_date=due_date,
            billing_period=customer["billing_period"],
            status=status,
            payment_link=generate_payment_link(),
            call_attempts=1 if status == BillStatus.CALLED else 0,
            payment_date=datetime.now() if status == BillStatus.PAID else None,
            payment_id=f"PAY{uuid.uuid4().hex[:12].upper()}" if status == BillStatus.PAID else None
        )
        
        db.add(bill)
        bills_created += 1
        
        print(f"✅ Created bill for {customer['customer_name']} - ₹{customer['bill_amount']} - Status: {status.value}")
    
    # Commit all changes
    db.commit()
    db.close()
    
    print(f"\n🎉 Successfully created {bills_created} bills!")
    print(f"📊 Database seeded with sample data")
    print(f"\n💡 You can now:")
    print(f"   - View bills at: http://localhost:3000")
    print(f"   - Test API at: http://localhost:8000/docs")
    print(f"   - Initiate calls for pending bills")


if __name__ == "__main__":
    print("🌱 Seeding database with sample bills...")
    print("=" * 60)
    create_sample_bills()
