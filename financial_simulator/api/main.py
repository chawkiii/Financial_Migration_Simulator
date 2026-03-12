# financial_simulator/api/main.py

from fastapi import FastAPI

from financial_simulator.api.routes_simulation import router as simulation_router

app = FastAPI(
    title="Canada Financial Engine API",
    version="0.3.0"
)


@app.get("/")
def root():
    return {
        "service": "Canada Financial Engine",
        "version": "0.3.0"
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(simulation_router)
