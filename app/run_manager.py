import asyncio
import uuid
from typing import Dict, Any, List

from app.agents.planner import PlannerAgent
from app.agents.generator import GeneratorAgent
from app.agents.ranker import RankerAgent
from app.chemistry.rdkit_tools import compute_descriptors
from app.screening.filters import apply_filter
from app.screening.scoring import score
from app.models.run_input import RunInput

RUNS: Dict[str, Dict[str, Any]] = {}



async def start_background_run(run_input: RunInput) -> str:
    run_id = str(uuid.uuid4())

    RUNS[run_id] = {
        "status": "PENDING",
        "input": run_input,
        "plan": None,
        "result": None,
        "trace": [],
        "error": None
    }

    asyncio.create_task(run_async(run_id))
    return run_id


def get_run(run_id: str) -> Dict[str, Any]:
    return RUNS.get(run_id, {"error": "Run not found"})


# async pipeline

async def run_async(run_id: str):
    run = RUNS[run_id]
    run["status"] = "RUNNING"

    try:
        result = await run_pipeline(run)
        run["result"] = result
        run["status"] = "COMPLETED"

    except Exception as e:
        run["status"] = "FAILED"
        run["error"] = str(e)


async def run_pipeline(run: Dict[str, Any]) -> List[Dict[str, Any]]:
    run_input: RunInput = run["input"]

    planner = PlannerAgent()
    generator = GeneratorAgent()
    ranker = RankerAgent()

    # planning
    plan = planner.plan(run_input)
    run["plan"] = plan
    run["trace"].append({
        "step": "planner",
        "plan": plan
    })

    seeds = run_input.seeds
    final_candidates = []

    # agentic
    for round_idx in range(plan["rounds"]):
        await asyncio.sleep(0) 

        run["trace"].append({
            "step": "round_start",
            "round": round_idx,
            "seeds": seeds
        })

        smiles_list = generator.generate(
            seeds=seeds,
            n_candidates=plan["candidates_per_round"]
        )

        run["trace"].append({
            "step": "generator",
            "round": round_idx,
            "proposed_count": len(smiles_list)
        })

        scored_molecules = []

        for smiles in smiles_list:
            props = compute_descriptors(smiles)
            if not props:
                continue

            passed, violations = apply_filter(props, plan["filters"])
            if not passed:
                continue

            props["violations"] = violations
            props["score"] = score(props, violations, plan["scoring"])
            scored_molecules.append(props)

        run["trace"].append({
            "step": "screening",
            "round": round_idx,
            "passed": len(scored_molecules)
        })

        if not scored_molecules:
            break

        scored_molecules.sort(key=lambda x: x["score"], reverse=True)
        seeds = [m["smiles"] for m in scored_molecules[:5]]

        final_candidates = scored_molecules

    # ranking
    top_k = ranker.select(final_candidates, plan["top_k"])
    run["trace"].append({
        "step": "ranker",
        "top_k": top_k
    })

    return top_k
