from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, contact

app = FastAPI(
    title="PersonalPortfolioBackend",
    description="A REST API for my personal portfolio validations and data management",
    version="v1"
)

origins = [
    "http://localhost:3000", 
    "https://my-portfolio-frontend-liart.vercel.app"
]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Incluir el enrutador en la aplicación
app.include_router(chat.router)
app.include_router(contact.router)

# Ruta principal para verificar que la app esté activa
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI!"}

# Run with uvicorn main:app --reload --host 127.0.0.1 --port 8000
# http://127.0.0.1:8000/docs#/ for SwaggerUI and api docs
