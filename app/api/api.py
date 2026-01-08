from fastapi import APIRouter
from app.models.run_input import RunInput
from app.run_manager import RUNS, start_background_run

router = APIRouter()


@router.post("/runs")
async def create_run(run_input: RunInput):
    run_id = await start_background_run(run_input)
    return {
        "run_id": run_id,
        "status": "PENDING"
    }
@router.get("/runs/{run_id}")
def get_run(run_id: str):
    return RUNS.get(run_id)
