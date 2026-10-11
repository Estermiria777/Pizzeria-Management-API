from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from models import UserRole, OrderStatus


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    address: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    address: Optional[str] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str


class PizzaSizeResponse(BaseModel):
    id: int
    name: str
    max_flavors: int
    price: float

    class Config:
        from_attributes = True

class CrustResponse(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True

class FlavorResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    category: str

    class Config:
        from_attributes = True


class OrderItemCreate(BaseModel):
    size_id: int
    crust_id: Optional[int] = None
    flavor_ids: List[int] = Field(..., min_items=1)
    quantity: int = 1
    notes: Optional[str] = None

class OrderCreate(BaseModel):
    delivery_address: str
    items: List[OrderItemCreate]

class OrderItemResponse(BaseModel):
    id: int
    size: PizzaSizeResponse
    crust: Optional[CrustResponse] = None
    flavors: List[FlavorResponse]
    quantity: int
    price: float
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    total_price: float
    delivery_address: str
    current_latitude: Optional[float] = None
    current_longitude: Optional[float] = None
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True