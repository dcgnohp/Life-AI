def score(props: dict, violations: int, scoring_cfg: dict) -> float:
    method = scoring_cfg.get("method")

    if method == "qed_penalty":
        penalty = scoring_cfg.get("penalty", 0.0)
        qed = props.get("qed", 0.0)
        return qed - penalty * violations

    raise ValueError(f"Invalid scoring method: {method}")
