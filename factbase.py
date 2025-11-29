# factbase.py

from typing import Iterable, Dict, Set

class FactBase:
    def __init__(self, initial_facts: Iterable[str] = None, enable_sources: bool = True):
        self.facts: Set[str] = set()
        self.sources: Dict[str, str] = {} if enable_sources else None
        if initial_facts:
            self.extend(initial_facts, source="initial")

    def _normalize(self, fact: str) -> str:
        return fact.strip().lower()

    def add(self, fact: str, source: str = "inferred") -> bool:
        """Add single fact. Returns True if added (was new)."""
        if not fact:
            return False
        f = self._normalize(fact)
        if not f:
            return False
        if f not in self.facts:
            self.facts.add(f)
            if self.sources is not None:
                self.sources[f] = source
            return True
        # If already present, optionally update source priority (skip for simplicity)
        return False

    def extend(self, facts: Iterable[str], source: str = "user") -> int:
        """Add many facts. Returns number of new facts added."""
        count = 0
        for fact in facts:
            if self.add(fact, source=source):
                count += 1
        return count

    def contains(self, fact: str) -> bool:
        return self._normalize(fact) in self.facts

    def as_list(self):
        return sorted(self.facts)

    def __iter__(self):
        return iter(self.facts)

    def __repr__(self):
        return f"FactBase({self.as_list()})"
