# financial_simulator/api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from financial_simulator.api.routes_simulation import router as simulation_router

app = FastAPI(
    title="Canada Financial Engine API",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"service": "Canada Financial Engine"}

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(simulation_router)