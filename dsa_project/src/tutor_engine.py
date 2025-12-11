"""
tutor_engine.py
----------------
High-level "DSA Tutor" engine built on top of the DSA Knowledge Graph.

Responsibilities:
    - Load the knowledge graph JSON
    - Use KnowledgeGraphSearch for concept lookup
    - Map free-text questions to the most relevant concept
    - Generate a structured, human-readable explanation

This module is:
    - LLM-free (no external API required)
    - Deterministic (only uses the local JSON KG)
    - Reusable (CLI, Streamlit, notebooks, etc.)
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Any, Dict, Optional

from src.search_engine import KnowledgeGraphSearch


class DsaTutorEngine:
    """
    High-level DSA tutor.

    Usage example
    -------------
    >>> engine = DsaTutorEngine("data/knowledge_graph.json")
    >>> result = engine.answer("Explain binary search")
    >>> print(result["answer_markdown"])
    """

    def __init__(self, graph_file: str | Path = "data/knowledge_graph.json") -> None:
        self.graph_file = Path(graph_file)
        if not self.graph_file.exists():
            raise FileNotFoundError(f"Knowledge graph file not found: {self.graph_file}")

        # Load raw KG
        with self.graph_file.open("r", encoding="utf-8") as f:
            self.kg: Dict[str, Dict[str, Any]] = json.load(f)

        # Search engine over KG
        self.engine = KnowledgeGraphSearch(self.graph_file)

    # ------------------------------------------------------------------ #
    # INTERNAL HELPERS
    # ------------------------------------------------------------------ #

    def _build_concept_explanation(self, concept: Dict[str, Any]) -> str:
        """
        Build a markdown explanation for a single concept node
        using only fields from the knowledge graph.
        """
        if not concept:
            return "I could not find any information for this concept."

        name = concept.get("name", "Unknown")
        ctype = concept.get("type", "N/A")
        category = concept.get("category", "N/A")
        ops = concept.get("basic_ops", []) or []
        uses = concept.get("use_cases", []) or []
        rels = concept.get("relations", []) or []
        desc = (concept.get("description", "") or "").strip()

        lines = []

        # Title
        lines.append(f"### 📘 {name}")
        lines.append("")
        lines.append(f"- **Type:** `{ctype}`")
        lines.append(f"- **Category:** `{category}`")

        if ops:
            ops_str = ", ".join(f"`{op}`" for op in ops)
            lines.append(f"- **Core operations:** {ops_str}")

        if uses:
            uses_str = ", ".join(f"`{u}`" for u in uses)
            lines.append(f"- **Typical use cases:** {uses_str}")

        if rels:
            rels_str = ", ".join(f"`{r}`" for r in rels)
            lines.append(f"- **Relations / tags:** {rels_str}")

        if desc:
            lines.append("")
            lines.append("#### 📖 Explanation")
            wrapped = textwrap.fill(desc, width=90)
            lines.append(wrapped)

        return "\n".join(lines)

    def _pick_best_concept_from_results(
        self,
        results: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """
        Given the result from engine.comprehensive_search(query),
        choose the most relevant concept node to explain.
        """
        # 1) Exact match
        if results.get("exact"):
            return results["exact"]

        # 2) Fuzzy: pick best score
        fuzzy = results.get("fuzzy") or {}
        if fuzzy:
            best_key = sorted(
                fuzzy.keys(),
                key=lambda k: fuzzy[k].get("match_score", 0.0),
                reverse=True,
            )[0]
            return self.kg.get(best_key)

        # 3) Keyword search: pick first hit
        keyword_hits = results.get("keyword") or {}
        if keyword_hits:
            first_key = list(keyword_hits.keys())[0]
            return self.kg.get(first_key)

        return None

    def _study_tip_for_category(self, category: str) -> Optional[str]:
        """
        Optional study tip based on concept category.
        """
        c = (category or "").lower()

        if c == "data_structure":
            return (
                "💡 **Study tip:** For data structures, practice implementing the core "
                "operations (insert, delete, search) and analyse their time complexity."
            )
        if c == "algorithm":
            return (
                "💡 **Study tip:** For algorithms, make sure you understand both the "
                "step-by-step procedure *and* the Big-O complexity. Trace small examples by hand."
            )
        return None

    # ------------------------------------------------------------------ #
    # PUBLIC METHODS
    # ------------------------------------------------------------------ #

    def explain_concept(self, concept_name: str) -> Dict[str, Any]:
        """
        Directly explain a concept by name.

        Returns:
            dict with keys:
                - query
                - matched_key
                - match_source   ("exact" | "fuzzy" | "keyword" | "none")
                - concept        (dict or None)
                - answer_markdown (str)
        """
        query = concept_name.strip()
        if not query:
            return {
                "query": concept_name,
                "matched_key": None,
                "match_source": "none",
                "concept": None,
                "answer_markdown": "Please provide a non-empty concept name.",
            }

        results = self.engine.comprehensive_search(query)
        concept = self._pick_best_concept_from_results(results)

        if concept is None:
            msg = f"I couldn't find a clear match for **{query}** in the knowledge graph."
            return {
                "query": query,
                "matched_key": None,
                "match_source": "none",
                "concept": None,
                "answer_markdown": msg,
            }

        # Find the matched key (if possible)
        matched_key = None
        for key, data in self.kg.items():
            if data is concept:
                matched_key = key
                break

        answer = self._build_concept_explanation(concept)

        tip = self._study_tip_for_category(concept.get("category", ""))
        if tip:
            answer += "\n\n" + tip

        # Determine source heuristically
        if results.get("exact") is concept:
            src = "exact"
        else:
            fuzzy = results.get("fuzzy") or {}
            if matched_key and matched_key in fuzzy:
                src = "fuzzy"
            else:
                src = "keyword"

        return {
            "query": query,
            "matched_key": matched_key,
            "match_source": src,
            "concept": concept,
            "answer_markdown": answer,
        }

    def answer(self, user_query: str) -> Dict[str, Any]:
        """
        Main entry point: answer a free-text question.

        Heuristics:
            - If query starts with "explain ", "what is ", "define ",
              we treat the rest as a concept name.
            - Otherwise, we search with the full query and map to the
              best concept.

        Returns:
            dict with keys:
                - query
                - matched_key
                - match_source
                - concept
                - answer_markdown
        """
        query_clean = user_query.strip()
        if not query_clean:
            return {
                "query": user_query,
                "matched_key": None,
                "match_source": "none",
                "concept": None,
                "answer_markdown": "Please type a question or a concept name.",
            }

        lowered = query_clean.lower()
        for prefix in ["explain ", "what is ", "define "]:
            if lowered.startswith(prefix):
                concept_name = query_clean[len(prefix):].strip()
                return self.explain_concept(concept_name)

        # Generic case: use full query
        results = self.engine.comprehensive_search(query_clean)
        concept = self._pick_best_concept_from_results(results)

        if concept is None:
            msg = (
                "I couldn't map your question to a specific concept in the knowledge graph.\n\n"
                "Try asking something like:\n"
                "- `Explain stack`\n"
                "- `What is binary search?`\n"
                "- `Define adjacency list`\n"
            )
            return {
                "query": query_clean,
                "matched_key": None,
                "match_source": "none",
                "concept": None,
                "answer_markdown": msg,
            }

        # Reuse explain_concept logic for consistency
        concept_name = concept.get("name", "")
        return self.explain_concept(concept_name)


# --------------------------------------------------------------------------- #
# SIMPLE MANUAL TEST
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    """
    Quick manual test:
        python -m src.tutor_engine
    """
    engine = DsaTutorEngine("data/knowledge_graph.json")

    test_queries = [
        "Explain stack",
        "what is binary search?",
        "define adjacency list",
        "how do trees work?",
        "shortest path algorithm",
    ]

    for q in test_queries:
        print("\n===============================================")
        print(f"QUERY: {q!r}")
        res = engine.answer(q)
        print(f"- Match source: {res['match_source']}")
        print(f"- Matched key: {res['matched_key']}")
        print(res["answer_markdown"])
