from pydantic import BaseModel, EmailStr, validator, constr
from datetime import datetime
from typing import List, Optional
from .models import OrderStatus
import re

class BookingCreate(BaseModel):
    name: str = constr(min_length=1, strip_whitespace=True)
    email: EmailStr
    phone_number: str
    total_person: int
    booking_date: datetime
    message: Optional[str] = None

    @validator('booking_date')
    def validate_booking_date(cls, v):
        if v < datetime.utcnow():
            raise ValueError('Booking date must be in the future')
        return v

    @validator('phone_number')
    def validate_phone_number(cls, v):
        # Basic validation for international or local numbers
        if not re.match(r'^\+?1?\d{9,15}$', v):
            raise ValueError('Invalid phone number format')
        return v

class BookingResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_number: str
    total_person: int
    booking_date: datetime
    message: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

class OrderItemCreate(BaseModel):
    item_name: str
    quantity: int
    price: float

    @validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be greater than zero')
        return v

class OrderItemResponse(BaseModel):
    id: int
    item_name: str
    quantity: int
    price: float

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    customer_name: str = constr(min_length=1, strip_whitespace=True)
    phone: str
    items: List[OrderItemCreate]

    @validator('phone')
    def validate_phone(cls, v):
        if not re.match(r'^\+?1?\d{9,15}$', v):
            raise ValueError('Invalid phone format')
        return v

    @validator('items')
    def validate_items(cls, v):
        if not v or len(v) == 0:
            raise ValueError('Order must contain at least one item')
        return v

class OrderResponse(BaseModel):
    id: int
    customer_name: str
    phone: str
    status: OrderStatus
    total_amount: float
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        orm_mode = True

class OrderStatusUpdate(BaseModel):
    status: OrderStatus
