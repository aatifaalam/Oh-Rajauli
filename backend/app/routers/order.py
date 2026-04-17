from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, db
from ..services import order_service

router = APIRouter(
    prefix="/api/orders",
    tags=["orders"]
)

@router.post("", response_model=schemas.OrderResponse, status_code=201)
def create_order(order: schemas.OrderCreate, db_session: Session = Depends(db.get_db)):
    return order_service.create_order(db=db_session, order=order)

@router.get("", response_model=List[schemas.OrderResponse])
def read_orders(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    orders = order_service.get_orders(db=db_session, skip=skip, limit=limit)
    return orders

@router.get("/{order_id}", response_model=schemas.OrderResponse)
def read_order(order_id: int, db_session: Session = Depends(db.get_db)):
    db_order = order_service.get_order(db=db_session, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.patch("/{order_id}/status", response_model=schemas.OrderResponse)
def update_order_status(order_id: int, status_update: schemas.OrderStatusUpdate, db_session: Session = Depends(db.get_db)):
    return order_service.update_order_status(db=db_session, order_id=order_id, status_update=status_update)
