from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException

def create_order(db: Session, order: schemas.OrderCreate):
    # Calculate total amount
    total_amount = sum(item.price * item.quantity for item in order.items)

    db_order = models.Order(
        customer_name=order.customer_name,
        phone=order.phone,
        total_amount=total_amount,
        status=models.OrderStatus.pending
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Add items
    for item in order.items:
        db_item = models.OrderItem(
            order_id=db_order.id,
            item_name=item.item_name,
            quantity=item.quantity,
            price=item.price
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).order_by(models.Order.created_at.desc()).offset(skip).limit(limit).all()

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def update_order_status(db: Session, order_id: int, status_update: schemas.OrderStatusUpdate):
    db_order = get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db_order.status = status_update.status
    db.commit()
    db.refresh(db_order)
    return db_order
