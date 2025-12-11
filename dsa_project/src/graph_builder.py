"""
graph_builder.py
----------------
Builds the complete DSA Knowledge Graph from:

1. Manual base metadata (base_concepts.py)
2. Semi-automatic descriptions (scraper.py)
3. Automatic relation inference
4. Automatic use-case generation
5. Export to JSON

Fully used by CLI, Streamlit, and report.
"""

from __future__ import annotations

import json
import argparse
from pathlib import Path
from typing import Dict, Any, List

from data.base_concepts import BASE_CONCEPTS
from src.scraper import fetch_description


# ---------------------------------------------------------------------------
# RELATION LOGIC
# ---------------------------------------------------------------------------
def generate_auto_relations(concept_name: str, base_data: Dict[str, Any]) -> List[str]:
    name = concept_name.lower()
    relations = []

    if any(w in name for w in ["array", "matrix", "list", "vector"]):
        relations += ["linear_structure", "sequential_access"]

    if "linked" in name:
        relations += ["pointer_based", "dynamic_structure"]

    if "stack" in name:
        relations += ["lifo_structure", "recursion_support"]

    if "queue" in name:
        relations += ["fifo_structure", "scheduling"]

    if "tree" in name:
        relations += ["hierarchical_structure", "recursion"]

    if "graph" in name:
        relations += ["network_structure", "traversal_bfs_dfs"]

    if "sparse" in name:
        relations += ["compressed_representation"]

    if "search" in name:
        relations += ["lookup_operation"]

    if "sort" in name:
        relations += ["ordering"]

    if "bfs" in name or "dfs" in name:
        relations += ["graph_traversal"]

    if "dijkstra" in name or "bellman" in name:
        relations += ["shortest_path"]

    relations.append(base_data.get("category", "data_structure"))

    return sorted(set(relations))


# ---------------------------------------------------------------------------
# USE-CASE LOGIC
# ---------------------------------------------------------------------------
def generate_use_cases(concept_name: str) -> List[str]:
    n = concept_name.lower()

    if "stack" in n:
        return ["function_call_stack", "undo_operations"]

    if "queue" in n:
        return ["task_scheduling", "bfs_traversal"]

    if "tree" in n:
        return ["hierarchical_data", "database_indexing"]

    if "sort" in n:
        return ["data_ordering"]

    if "graph" in n:
        return ["network_routing"]

    if "matrix" in n or "sparse" in n:
        return ["scientific_computing"]

    return ["general_dsa_application"]


# ---------------------------------------------------------------------------
# BUILD KNOWLEDGE GRAPH
# ---------------------------------------------------------------------------
def build_knowledge_graph(output="data/knowledge_graph.json", enrich=True):
    print("\n[GRAPH_BUILDER] Building full DSA Knowledge Graph...")
    graph = {}

    for concept_key, base_data in BASE_CONCEPTS.items():
        print(f"[GRAPH_BUILDER] Processing: {concept_key}")

        node = dict(base_data)

        # DESCRIPTIONS
        node["description"] = (
            fetch_description(base_data["name"])
            if enrich else base_data.get("description", "")
        )

        # RELATIONS
        node["relations"] = generate_auto_relations(concept_key, base_data)

        # USE CASES
        node["use_cases"] = generate_use_cases(concept_key)

        # UNIQUE ID
        node["id"] = f"dsa_{concept_key}"

        graph[concept_key] = node

    # SAVE
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)

    print(f"[GRAPH_BUILDER] ✔ Saved graph to {out}")
    print(f"[GRAPH_BUILDER] ✔ Total concepts: {len(graph)}")
    return graph


# ---------------------------------------------------------------------------
# CLI WRAPPER
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Build the DSA Knowledge Graph.")
    parser.add_argument("--fast", action="store_true", help="Disable web scraping (debug mode)")
    parser.add_argument("--out", type=str, default="data/knowledge_graph.json")
    args = parser.parse_args()

    build_knowledge_graph(output=args.out, enrich=not args.fast)


if __name__ == "__main__":
    main()
