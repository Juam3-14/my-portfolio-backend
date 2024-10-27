from fastapi import APIRouter

router = APIRouter()

@router.post("/send_contact_message")
async def say_hello():
    return {"message": "Hello from FastAPI"}