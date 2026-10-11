from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Order, OrderItem, PizzaSize, Crust, Flavor, OrderStatus, User
from schemas import (
    OrderCreate, 
    OrderResponse, 
    PizzaSizeResponse, 
    CrustResponse, 
    FlavorResponse
)
from auth_routes import get_current_user

router = APIRouter(prefix="/orders", tags=["Pedidos & Cardápio"])


@router.get("/sizes", response_model=List[PizzaSizeResponse])
def list_sizes(db: Session = Depends(get_db)):
    return db.query(PizzaSize).all()

@router.get("/crusts", response_model=List[CrustResponse])
def list_crusts(db: Session = Depends(get_db)):
    return db.query(Crust).all()

@router.get("/flavors", response_model=List[FlavorResponse])
def list_flavors(db: Session = Depends(get_db)):
    return db.query(Flavor).all()



@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_order_price = 0.0
    db_items = []

    for item in order_data.items:
        
        size = db.query(PizzaSize).filter(PizzaSize.id == item.size_id).first()
        if not size:
            raise HTTPException(
                status_code=404, 
                detail=f"Tamanho ID {item.size_id} não encontrado."
            )

        
        if len(item.flavor_ids) > size.max_flavors:
            raise HTTPException(
                status_code=400,
                detail=f"O tamanho {size.name} permite no máximo {size.max_flavors} sabores."
            )

        
        unique_flavor_ids = list(set(item.flavor_ids))
        flavors = db.query(Flavor).filter(Flavor.id.in_(unique_flavor_ids)).all()
        
        if len(flavors) != len(unique_flavor_ids):
            raise HTTPException(
                status_code=404, 
                detail="Um ou mais sabores selecionados não existem no cardápio."
            )

        
        crust_price = 0.0
        crust = None
        if item.crust_id:
            crust = db.query(Crust).filter(Crust.id == item.crust_id).first()
            if not crust:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Borda ID {item.crust_id} não encontrada."
                )
            crust_price = crust.price

        
        item_price = (size.price + crust_price) * item.quantity
        total_order_price += item_price

        
        order_item = OrderItem(
            size_id=size.id,
            crust_id=crust.id if crust else None,
            quantity=item.quantity,
            price=item_price,
            notes=item.notes,
            flavors=flavors
        )
        db_items.append(order_item)

    
    new_order = Order(
        user_id=current_user.id,
        status=OrderStatus.PENDING,
        total_price=total_order_price,
        delivery_address=order_data.delivery_address,
        items=db_items
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order



@router.get("/my-orders", response_model=List[OrderResponse])
def get_user_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Order).filter(Order.user_id == current_user.id).all()