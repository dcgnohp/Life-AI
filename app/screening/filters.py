def apply_filter(props: dict, filters: dict):
    violations = 0
    failure_reasons = []

    if props["mw"] > filters["mw"]:
        violations += 1
        failure_reasons.append("mw")

    if props["logp"] > filters["logp"]:
        violations += 1
        failure_reasons.append("logp")

    if props["hbd"] > filters["hbd"]:
        violations += 1
        failure_reasons.append("hbd")

    if props["hba"] > filters["hba"]:
        violations += 1
        failure_reasons.append("hba")

    if props["tpsa"] > filters["tpsa"]:
        violations += 1
        failure_reasons.append("tpsa")

    passed = violations <= filters["max_violations"]
    return passed, violations
