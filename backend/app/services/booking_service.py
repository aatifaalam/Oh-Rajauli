from sqlalchemy.orm import Session
from .. import models, schemas
from datetime import datetime

def create_booking(db: Session, booking: schemas.BookingCreate):
    db_booking = models.Booking(
        name=booking.name,
        email=booking.email,
        phone_number=booking.phone_number,
        total_person=booking.total_person,
        booking_date=booking.booking_date,
        message=booking.message
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).order_by(models.Booking.created_at.desc()).offset(skip).limit(limit).all()
