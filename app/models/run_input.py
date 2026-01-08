from pydantic import BaseModel, Field
from typing import List, Dict


class FiltersConfig(BaseModel):
    mw: float = 500
    logp: float = 5
    hbd: int = 5
    hba: int = 10
    tpsa: float = 140
    max_violations: int = 1


class GeneratorConfig(BaseModel):
    candidates_per_round: int = Field(..., gt=0)


class ScoringConfig(BaseModel):
    method: str = "qed_penalty"
    penalty: float = 0.1


class RunInput(BaseModel):
    objective: str
    seeds: List[str]

    rounds: int = Field(1, gt=0)
    top_k: int = Field(1, gt=0)

    filters: FiltersConfig
    generator: GeneratorConfig
    scoring: ScoringConfig
