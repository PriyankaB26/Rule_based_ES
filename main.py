from factbase import FactBase
from rules import rules
from engine import forward_chain
import difflib

# ---------- Pretty printer ----------
def pretty_print_results(user_facts: list, fact_base, inference_log: list):
    # User facts (in original order)
    print("\nUser facts:")
    for f in user_facts:
        print(f"- {f} (user)")

    # Inference steps
    print("\nInference steps:")
    if not inference_log:
        print("No rules fired.")
    else:
        for entry in inference_log:
            step = entry["step"]
            rule_id = entry["rule_id"]
            antecedents = entry["antecedents"]
            consequent = entry["consequent"]
            explanation = entry.get("explanation", "")
            added = entry["added_new"]

            ant_text = " & ".join(antecedents)
            add_text = "added" if added else "no change"
            source_text = f"(inferred_by:{rule_id})" if added else "(no change)"

            print(f"{step}) {rule_id}: IF {ant_text} THEN {consequent} — {add_text} {source_text}")
            if explanation:
                print(f"   Explanation: {explanation}")
            # Facts now (snapshot)
            facts_now = entry.get("fact_snapshot", sorted(fact_base.facts))
            print(f"   Facts now: {', '.join(facts_now)}\n")

        # === Final facts (grouped by source) ===
    user_final = []
    inferred_final = []
    unknown_final = []

    for f in sorted(fact_base.facts):
        src = None
        if hasattr(fact_base, "sources") and fact_base.sources is not None:
            src = fact_base.sources.get(f, None)

        if src == "user":
            user_final.append(f)
        elif src and src.startswith("inferred_by"):
            inferred_final.append(f)
        else:
            unknown_final.append(f)

    print("Final Facts (Grouped):")

    if user_final:
        print("\nUser-entered facts:")
        for f in user_final:
            print(f"- {f}")

    if inferred_final:
        print("\nInferred facts:")
        for f in inferred_final:
            print(f"- {f}")

    if unknown_final:
        print("\nUnknown-source facts:")
        for f in unknown_final:
            print(f"- {f}")


# ---------- Canonical vocabulary + synonyms ----------
CANONICAL = {
    "fever", "cough", "sore throat", "runny nose", "sneezing",
    "body ache", "fatigue", "dry cough", "loss of taste", "loss of smell",
    "stomach pain", "vomiting", "diarrhea", "acidity", "burning chest",
    "sour taste", "headache", "sensitivity to light", "nausea",
    "stress", "blurred vision", "burning urination", "frequent urination",
    "lower abdominal pain", "chest pain", "shortness of breath", "wheezing",
    "chronic cough", "weight loss", "weakness", "pale skin",
    "unexplained weight loss", "loss of appetite", "increased thirst",
    "sudden numbness", "one side weakness", "facial droop", "slurred speech",
    "yellow skin", "yellow eyes", "unusual bruising", "frequent bleeding",
    "persistent sadness", "hopelessness", "restlessness", "excessive worry",
    "chills", "muscle aches"
}

SYNONYMS = {
    "sour throat": ["sore throat"],
    "sorethroat": ["sore throat"],
    "sore-throat": ["sore throat"],
    "cold": ["runny nose", "sneezing"],
    "common cold": ["runny nose", "sneezing"],
    "sob": ["shortness of breath"],
    "breathlessness": ["shortness of breath"],
    "feverish": ["fever"],
    "high temperature": ["fever"],
    "vomit": ["vomiting"],
    "pale": ["pale skin"],
    "wt loss": ["unexplained weight loss"],
    "weightloss": ["unexplained weight loss"],
    "loss of taste or smell": ["loss of taste", "loss of smell"]
}

def normalize_token(tok: str) -> str:
    return tok.strip().lower()

def expand_fact(tok: str):
    """Return a list of canonical facts for a user token."""
    t = normalize_token(tok)
    if not t:
        return []
    # direct synonym mapping
    if t in SYNONYMS:
        return SYNONYMS[t]
    # exact canonical
    if t in CANONICAL:
        return [t]
    # fuzzy-match to canonical set (helps with small typos)
    close = difflib.get_close_matches(t, list(CANONICAL), n=1, cutoff=0.82)
    if close:
        return [close[0]]
    # if nothing matches, return the raw token as-is (still recorded)
    return [t]

# ---------- Main ----------
if __name__ == "__main__":
    # 1. collect user input
    user_input = input("Enter symptoms (comma separated): ")

    # 2. parse raw tokens and expand synonyms / fuzzy matches
    raw_tokens = [p.strip() for p in user_input.replace(";", ",").split(",") if p.strip()]
    expanded = []
    for t in raw_tokens:
        mapped = expand_fact(t)
        # show mapping for transparency when it changes the token
        if len(mapped) > 1 or (len(mapped) == 1 and mapped[0] != t.strip().lower()):
            print(f"Mapping input '{t}' -> {mapped}")
        expanded.extend(mapped)

    user_facts = [f.strip().lower() for f in expanded if f.strip()]
    print("Normalized/expanded user facts:", user_facts)

    # 3. build fact base and add user facts
    fb = FactBase()
    fb.extend(user_facts, source="user")

    # 4. Normalize rules BEFORE running engine (important)
    for i, r in enumerate(rules):
        r["if"] = [a.strip().lower() for a in r.get("if", [])]
        r["then"] = r.get("then", "").strip().lower()
        if "id" not in r:
            r["id"] = f"R{i+1}"
        if "explanation" not in r:
            r["explanation"] = ""

    # 5. Debug prints to verify what's loaded
    #print("\nDEBUG: user_facts =", user_facts)
    #print("DEBUG: fact_base.facts before chaining =", sorted(fb.facts))
    #print("DEBUG: first 10 normalized rules (id, if -> then):")
    #for r in rules[:10]:
     #   print(f"  {r['id']}: IF {r['if']} THEN {r['then']}")

    # 6. run forward chaining
    final_facts, log = forward_chain(rules, fb, stop_on=None)

    # 7. pretty print results
    pretty_print_results(user_facts, fb, log)
