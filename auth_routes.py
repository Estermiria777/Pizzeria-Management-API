from fastapi import APIRouter

auth_router = APIRouter(prefix = "/auth", tags = ["auth"])

@auth_router.get("/")
async def authenticate():
    """
    This is the authenticate standard route of my system
    """
    return { "mensage": "You have accessed the authenticate standard route", "authenticate": False }
