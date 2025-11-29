from typing import List, Dict, Tuple, Set, Iterable

def apply_rules_once(rules: Iterable[Dict], fact_base, fired_rules: Set[str]) -> List[Dict]:
    """
    Apply every rule once against the fact_base, skipping already fired rules.
    Returns a list of entries describing which rules matched and whether they added new facts.
    Each entry:
      {
        "rule_id": str,
        "antecedents": [...],
        "consequent": str,
        "explanation": str,
        "matched": bool,
        "added_new": bool
      }
    """
    log = []

    for idx, rule in enumerate(rules):
        rule_id = rule.get("id", f"R{idx+1}")
        antecedents = [a.strip().lower() for a in rule.get("if", [])]
        consequent = rule.get("then", "").strip().lower()
        explanation = rule.get("explanation", "")

        if rule_id in fired_rules:
            #skip rules already fired
            continue

        applicable = all(a in fact_base.facts for a in antecedents)

        entry = {
            "rule_id": rule_id,
            "antecedents": antecedents,
            "consequent": consequent,
            "explanation": explanation,
            "matched": applicable,
            "added_new": False
        }

        if applicable and consequent:
            # Attempt to add the consequent to the fact base
            # FactBase.add should return True if fact was newly added
            try:
                added = fact_base.add(consequent, source=f"inferred_by:{rule_id}")
            except TypeError:
                # Fall back if add doesn't accept source param
                added = fact_base.add(consequent)
            if added:
                entry["added_new"] = True
            # Whether added or not, mark rule as fired to avoid re-evaluating it
            fired_rules.add(rule_id)

        log.append(entry)

    return log

def forward_chain(rules: Iterable[Dict], fact_base, stop_on: Iterable[str] = None, max_iterations: int = 1000) -> Tuple[Set[str], List[Dict]]:
    """
    Full forward-chaining loop.
    Returns (final_facts_set, chronological_inference_log)
    Each log entry has:
      { step, rule_id, antecedents, consequent, added_new, fact_snapshot, explanation, sources(optional) }
    """
    stop_on = {s.strip().lower() for s in (set(stop_on) if stop_on else set())}
    inference_log: List[Dict] = []
    fired_rules: Set[str] = set()
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        pass_log = apply_rules_once(rules, fact_base, fired_rules)

        # If no rules matched or no new facts were added in this pass, stop
        if not any(entry["added_new"] for entry in pass_log):
            break

        # Append chronological log entries for those that added new facts
        for entry in pass_log:
            if entry["matched"] and entry["consequent"]:
                step_log = {
                    "step": len(inference_log) + 1,
                    "rule_id": entry["rule_id"],
                    "antecedents": entry["antecedents"],
                    "consequent": entry["consequent"],
                    "added_new": entry["added_new"],
                    "fact_snapshot": sorted(fact_base.facts),
                    "explanation": entry.get("explanation", "")
                }
                # include sources map if available
                if hasattr(fact_base, "sources") and fact_base.sources is not None:
                    step_log["sources"] = {f: fact_base.sources.get(f, None) for f in step_log["fact_snapshot"]}
                inference_log.append(step_log)

        # stop early if target facts achieved
        if stop_on and stop_on.issubset(fact_base.facts):
            break

    return set(fact_base.facts), inference_log