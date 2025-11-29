from typing import List, Dict, Tuple, Set, Iterable

def _classify_source(src: str) -> str:
    """Normalize source string to a short label."""
    if not src:
        return "unknown"
    src = src.lower()
    if src == "user" or src == "initial":
        return "user"
    if src.startswith("inferred_by:"):
        return "inferred"
    if src.startswith("possible_inferred_by:"):
        return "possible_inferred"
    # fallback
    return src

def apply_rules_once(rules: Iterable[Dict], fact_base, fired_rules: Set[str]) -> List[Dict]:
    """
    Apply every rule once against the fact_base, skipping already fired rules.
    Returns a list of entries describing which rules matched and whether they added new facts.
    Each entry includes:
      - rule_id, antecedents, consequent, explanation
      - matched: bool (all antecedents present)
      - matched_antecedents: list of antecedents that were present
      - antecedent_status: dict mapping antecedent -> present(bool)
      - antecedent_sources: dict mapping antecedent -> source label (user|inferred|possible_inferred|unknown)
      - added_new: bool
      - fact_snapshot: list (captured immediately after adding consequent)
    """
    log = []

    for idx, rule in enumerate(rules):
        rule_id = rule.get("id", f"R{idx+1}")
        antecedents = [a.strip().lower() for a in rule.get("if", [])]
        consequent = rule.get("then", "").strip().lower()
        explanation = rule.get("explanation", "")

        if rule_id in fired_rules:
            # skip already-fired rules
            continue

        # Determine which antecedents are present and collect sources
        antecedent_status = {}
        antecedent_sources = {}
        matched_antecedents = []
        for a in antecedents:
            present = a in fact_base.facts
            antecedent_status[a] = present
            if present:
                matched_antecedents.append(a)
            # find source from fact_base.sources if available
            src = None
            if hasattr(fact_base, "sources") and fact_base.sources is not None:
                src = fact_base.sources.get(a, None)
            antecedent_sources[a] = _classify_source(src)

        # A rule is applicable (full match) only if all antecedents present
        applicable = all(antecedent_status.values()) if antecedents else False

        entry = {
            "rule_id": rule_id,
            "antecedents": antecedents,
            "consequent": consequent,
            "explanation": explanation,
            "matched": applicable,
            "matched_antecedents": matched_antecedents,
            "antecedent_status": antecedent_status,
            "antecedent_sources": antecedent_sources,
            "added_new": False,
            "fact_snapshot": None
        }

        if applicable and consequent:
            # Attempt to add the consequent to the fact base immediately
            try:
                added = fact_base.add(consequent, source=f"inferred_by:{rule_id}")
            except TypeError:
                added = fact_base.add(consequent)

            if added:
                entry["added_new"] = True

            # Mark as fired so it won't be re-evaluated
            fired_rules.add(rule_id)

            # Capture snapshot immediately after adding consequent
            entry["fact_snapshot"] = sorted(fact_base.facts)

        log.append(entry)

    return log


def forward_chain(rules: Iterable[Dict], fact_base, stop_on: Iterable[str] = None, max_iterations: int = 1000) -> Tuple[Set[str], List[Dict]]:
    """
    Full forward-chaining loop with antecedent-source-aware logging.
    Returns (final_facts_set, chronological_inference_log).
    Each log entry includes:
      - step
      - rule_id
      - antecedents
      - consequent
      - added_new (bool)
      - fact_snapshot (list)
      - explanation
      - matched_antecedents
      - antecedent_status
      - antecedent_sources
    """
    stop_on = {s.strip().lower() for s in (set(stop_on) if stop_on else set())}
    inference_log: List[Dict] = []
    fired_rules: Set[str] = set()
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        pass_log = apply_rules_once(rules, fact_base, fired_rules)

        # If no new facts were added, stop
        if not any(entry["added_new"] for entry in pass_log):
            break

        # Append chronological log entries (only for entries that added a fact)
        for entry in pass_log:
            if entry["matched"] and entry["consequent"] and entry["added_new"]:
                step_log = {
                    "step": len(inference_log) + 1,
                    "rule_id": entry["rule_id"],
                    "antecedents": entry["antecedents"],
                    "consequent": entry["consequent"],
                    "added_new": entry["added_new"],
                    "fact_snapshot": entry.get("fact_snapshot", sorted(fact_base.facts)),
                    "explanation": entry.get("explanation", ""),
                    "matched_antecedents": entry.get("matched_antecedents", []),
                    "antecedent_status": entry.get("antecedent_status", {}),
                    "antecedent_sources": entry.get("antecedent_sources", {})
                }
                inference_log.append(step_log)

        # stop early if requested targets are present
        if stop_on and stop_on.issubset(fact_base.facts):
            break

    return set(fact_base.facts), inference_log
