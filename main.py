from fastapi import FastAPI
from database import Base, engine
import order_routes
import auth_routes


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pizzeria Management API")

app.include_router(auth_routes.router) 
app.include_router(order_routes.router)