from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, db
from ..services import booking_service

router = APIRouter(
    prefix="/api/bookings",
    tags=["bookings"]
)

@router.post("", response_model=schemas.BookingResponse, status_code=201)
def create_booking(booking: schemas.BookingCreate, db_session: Session = Depends(db.get_db)):
    return booking_service.create_booking(db=db_session, booking=booking)

@router.get("", response_model=List[schemas.BookingResponse])
def read_bookings(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    bookings = booking_service.get_bookings(db=db_session, skip=skip, limit=limit)
    return bookings
