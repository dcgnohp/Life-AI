from app.models.run_input import RunInput

class PlannerAgent:
    def plan(self, run_input: RunInput):
        return {
            "objective": run_input.objective,
            "rounds": run_input.rounds,
            "candidates_per_round": run_input.generator.candidates_per_round,
            "top_k": run_input.top_k,
            "filters": run_input.filters.model_dump(),
            "scoring": run_input.scoring.model_dump()
        }
