import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from database import Base

order_item_flavors = Table(
    'order_item_flavors',
    Base.metadata,
    Column('order_item_id', Integer, ForeignKey('order_items.id', ondelete="CASCADE"), primary_key=True),
    Column('flavor_id', Integer, ForeignKey('flavors.id', ondelete="CASCADE"), primary_key=True)
)

class UserRole(str, enum.Enum):
    CLIENT = "CLIENT"
    ADMIN = "ADMIN"
    DELIVERY = "DELIVERY"

class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"             
    PREPARING = "PREPARING"      
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY" 
    DELIVERED = "DELIVERED"        
    CANCELED = "CANCELED"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CLIENT, nullable=False)
    address = Column(String, nullable=True)

    orders = relationship("Order", back_populates="user")

class PizzaSize(Base):
    __tablename__ = "pizza_sizes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False) 
    max_flavors = Column(Integer, nullable=False, default=1) 
    price = Column(Float, nullable=False) 

class Crust(Base):
    __tablename__ = "crusts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False) 
    price = Column(Float, default=0.0)

class Flavor(Base):
    __tablename__ = "flavors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    category = Column(String, default="Salgada") 

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    total_price = Column(Float, nullable=False, default=0.0)
    delivery_address = Column(String, nullable=False)
    
    
    current_latitude = Column(Float, nullable=True)
    current_longitude = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    size_id = Column(Integer, ForeignKey("pizza_sizes.id"))
    crust_id = Column(Integer, ForeignKey("crusts.id"), nullable=True)
    quantity = Column(Integer, default=1)
    price = Column(Float, nullable=False) 
    notes = Column(String, nullable=True) 

    order = relationship("Order", back_populates="items")
    size = relationship("PizzaSize")
    crust = relationship("Crust")
    flavors = relationship("Flavor", secondary=order_item_flavors)