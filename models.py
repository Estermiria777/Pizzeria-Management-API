import enum
from sqlalchemy import Boolean, Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

# Cria a Base declarativa para os modelos
Base = declarative_base()


# 1. Definição do Enum (deve vir ANTES de ser usado nos modelos)
class OrderStatus(str, enum.Enum):
    PENDENTE = "PENDENTE"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"


# 2. Modelo de Usuários
class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False, unique=True)
    password = Column("password", String)
    active = Column("active", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin


# 3. Modelo de Pedidos (Orders)
class Order(Base):
    __tablename__ = "orders"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    price = Column("price", Float, default=0.0)
    status = Column(
        Enum(OrderStatus), default=OrderStatus.PENDENTE, nullable=False
    )
    user_id = Column("user_id", Integer, ForeignKey("users.id"))

    def __init__(self, user_id, status=OrderStatus.PENDENTE, price=0.0):
        self.user_id = user_id
        self.status = status
        self.price = price


# 4. Modelo de Itens do Pedido
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantity = Column("quantity", Integer)
    flavor = Column("flavor", String)
    size = Column("size", String)
    price_per_pizza = Column("price_per_pizza", Float)
    order_id = Column("order_id", Integer, ForeignKey("orders.id"))

    def __init__(self, quantity, flavor, size, price_per_pizza, order_id):
        self.quantity = quantity
        self.flavor = flavor
        self.size = size
        self.price_per_pizza = price_per_pizza
        self.order_id = order_id