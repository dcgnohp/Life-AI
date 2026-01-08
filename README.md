# LIFE AI – Agentic Molecule Generation & Screening Service

This project implements an asynchronous agentic pipeline simulating a simplified drug design workflow as described in the assignment.

## Features

- **Asynchronous Pipeline:** Start, monitor, and retrieve molecule design runs via API. Runs execute asynchronously (background task queue).

- **Agentic System Architecture:**
  - **Planner Agent:** Sets up experimental parameters (rounds, candidates/round, selection/filter constraints, etc.)
  - **Generator Agent:** Proposes new molecules (SMILES) by mutating given seeds (swap halogens, add/remove methyl group).
  - **Chemistry Tooling:** Uses RDKit to check validity and compute key descriptors for each SMILES (MW, LogP, HBD, HBA, TPSA, rotatable bonds, QED).
  - **Filter/Screening:** Configurable rule-based filters (Lipinski-like + TPSA), with up to `N` allowed violations.
  - **Scoring/Ranking:** Score = QED - 0.1 × [violations], or as configured; returns ranked molecules.
  - **Ranker Agent:** Selects final candidates and outputs structured trace.

- **API:** Exposes endpoints to start a run, check status/results, and get a decision trace.

## Tech Stack

- Python, FastAPI, Pydantic, RDKit

## Example Workflow

- **Input**
  - Objective: Generate drug-like molecules, maximize QED
  - Seeds: 2 starting SMILES
  - Filters: MW ≤ 500, LogP ≤ 5, HBD ≤ 5, HBA ≤ 10, TPSA ≤ 140
  - Max violations: 1

- **Generation**
  - Generator proposes new molecules via mutations

- **Descriptor Calculation**
  - RDKit computes core molecular properties

- **Screening**
  - Molecules failing more than allowed violations are discarded

- **Ranking**
  - Remaining molecules are scored and ranked
  - Top candidates are returned

- **Audit Trace**
  - Every step is recorded in a structured execution trace


## Setup Instructions

### 1. Install Python dependencies

First, ensure you have Python 3.8+ installed.

Install all dependencies (including RDKit, which might require `conda` on some platforms):

```bash
pip install -r requirements.txt
```

(If you have issues installing RDKit via pip, please refer to the [official RDKit installation guide](https://www.rdkit.org/docs/Install.html).)

### 2. Run the Service

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API docs will be automatically available at:  
http://127.0.0.1:8000/docs

### 3. Example API Usage

- **Start a new run:**  
  `POST /runs`  
  Supply a JSON body like:
  ```json
    {
    "objective": "Generate drug-like molecules; maximize QED; keep ≤ 1 rule violation.",
    "seeds": [
        "CCO",
        "c1ccccc1"
    ],
    "rounds": 1,
    "top_k": 3,
    "filters": {
        "mw": 500,
        "logp": 5,
        "hbd": 5,
        "hba": 10,
        "tpsa": 140,
        "max_violations": 1
    },
    "generator": {
        "candidates_per_round": 50
    },
    "scoring": {
        "method": "qed_penalty",
        "penalty": 0.1
    }
    }

  ```

- **Check run status/results:**  
  `GET /runs/{run_id}`  
  Retrieve full trace and top candidates.

## Design Notes

- **Scoring:** Default: `score = QED - 0.1 * [violations]` (see `app/screening/scoring.py`).
- **Filters:** Molecules passing with ≤ allowed violations (e.g., ≤1). See `app/screening/filters.py`.
- **Asynchronous Execution:** Uses Python's `asyncio` to ensure starting a new run never blocks.
- **Audit Trace:** Every run records a structured step-by-step trace for auditing & debugging.

## Directory Structure

```
app/
|--  agents/      # Planner, Generator, and Ranker agent policies
|--  api/         # FastAPI endpoints
|--  chemistry/   # RDKit utilities and descriptor calculations
|--  models/      # Pydantic data models/configs
|--  screening/   # Rule-based filters and scoring
|--  main.py      # App entry point (FastAPI init)
|--  run_manager.py # Orchestrates agentic loop, run queue, result/traces
requirements.txt
README.md
```
