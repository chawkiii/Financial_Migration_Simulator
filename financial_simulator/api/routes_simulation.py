# financial_simulator/api/routes_simulation.py

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from financial_simulator.core.inputs import build_inputs
from financial_simulator.core.simulation_pipeline import SimulationPipeline

from .schemas import SimulationRequest

router = APIRouter()


@router.post("/simulate")
def simulate(request: SimulationRequest):

    try:
        # =========================
        # BUILD INPUTS
        # =========================
        inputs = build_inputs(request)

        # =========================
        # RUN PIPELINE
        # =========================
        pipeline = SimulationPipeline()
        output = pipeline.run(inputs, run_monte_carlo=False)

        # =========================
        # SERIALIZATION SAFE
        # =========================
        result = output["projection"]

        response = {
            "summary": result.to_dict(),
            "tax": output["tax_summary"],
            "score": output["score"],
            "risk": output["risk"],
            "success_probability": output["success_probability"],
            "strategy": output["strategy"],
            "insights": output["insights"],
        }

        # ✅ CRUCIAL: convert everything to JSON-safe
        return jsonable_encoder(response)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Invalid key: {str(e)}")

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail="Internal server error")