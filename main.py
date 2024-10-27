from fastapi import FastAPI
from app.routers import chat

app = FastAPI()

# Incluir el enrutador en la aplicación
app.include_router(chat.router)

# Ruta principal para verificar que la app esté activa
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI!"}

# Run with uvicorn main:app --reload --host 127.0.0.1 --port 8000
# http://127.0.0.1:8000/docs#/ for SwaggerUI and api docs