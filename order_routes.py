from fastapi import APIRouter

order_router = APIRouter(prefix="/order", tags=["order"])

@order_router.get("/")
async def order():
    """
    This is the order standard path of my system. All the order's routes needs authentication
    """
    return {"mensage": "You have accessed the order path"}
