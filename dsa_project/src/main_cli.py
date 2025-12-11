"""
main_cli.py
-----------
Command-Line Interface for the DSA Knowledge Graph.

This interface demonstrates:
    - Exact search
    - Fuzzy search
    - Relation search
    - Keyword search
    - Combined search results
    - Help and statistics menu
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

from src.search_engine import KnowledgeGraphSearch


# =============================================================================
# FORMATTED OUTPUT HELPERS
# =============================================================================

def print_header(title: str) -> None:
    print("\n" + "=" * 60)
    print(f"{title}")
    print("=" * 60)


def print_concept(concept: Dict[str, Any]) -> None:
    """Pretty-print a concept node."""
    if not concept:
        print("No concept data available.")
        return

    print_header(f"📘 CONCEPT: {concept.get('name', 'Unknown').upper()}")

    print(f"ID:            {concept.get('id', 'N/A')}")
    print(f"Type:          {concept.get('type', 'N/A')}")
    print(f"Category:      {concept.get('category', 'N/A')}")

    # Basic operations
    ops = concept.get("basic_ops", [])
    if ops:
        print("\n⚙️  Basic Operations:")
        for op in ops:
            print(f"  - {op}")

    # Use Cases
    uses = concept.get("use_cases", [])
    if uses:
        print("\n📌 Use Cases:")
        for use in uses:
            print(f"  - {use}")

    # Relations
    rels = concept.get("relations", [])
    if rels:
        print("\n🔗 Relations:")
        for rel in rels:
            print(f"  - {rel}")

    # Description
    desc = concept.get("description", "")
    if desc:
        print("\n📖 Description:")
        print(f"  {desc[:400]}{'...' if len(desc) > 400 else ''}")


def print_fuzzy_results(results: Dict[str, Any]) -> None:
    if not results:
        return

    print("\n🤔 Possible matches:")
    for key, info in results.items():
        score = info.get("match_score", 0)
        print(f"  - {info['name']} (score={score:.2f})")


def print_related_results(results: Dict[str, Any]) -> None:
    if not results:
        return

    print("\n🔗 Related Concepts:")
    for key, info in results.items():
        relation_type = info.get("relation_type", "unknown")
        print(f"  - {info['name']} (via relation '{relation_type}')")


def print_keyword_results(results: Dict[str, Any]) -> None:
    if not results:
        return

    print("\n🔍 Keyword Matches:")
    for key, info in results.items():
        snippet = info.get("snippet", "")
        print(f"  - {info['name']}: {snippet}")


def show_help() -> None:
    print_header("HELP - AVAILABLE COMMANDS")
    print("""
Type any concept name to search, e.g.:
    stack
    binary search
    adjacency list
    recursion

Special commands:
    help    -> Show this help
    stats   -> Display graph statistics
    quit    -> Exit the program
""")


# =============================================================================
# MAIN LOOP
# =============================================================================

def main() -> None:
    print_header("🎓 DSA Knowledge Graph - CLI Interface")

    # Load search engine
    try:
        engine = KnowledgeGraphSearch("data/knowledge_graph.json")
    except FileNotFoundError:
        print("❌ Error: knowledge_graph.json not found. Build the graph first.")
        sys.exit(1)

    print("Type 'help' to see available commands.\n")

    while True:
        try:
            query = input("🔍 Enter a query: ").strip()

            if not query:
                continue

            # -------------------- SPECIAL COMMANDS --------------------
            if query.lower() == "quit":
                print("\n👋 Goodbye!")
                break

            if query.lower() == "help":
                show_help()
                continue

            if query.lower() == "stats":
                stats = engine.stats()
                print_header("📊 GRAPH STATISTICS")
                print(f"Concepts:       {stats['num_concepts']}")
                print(f"Relations:      {stats['num_relations']}")
                print(f"Source File:    {stats['graph_file']}")
                continue

            # -------------------- NORMAL SEARCH -----------------------
            results = engine.comprehensive_search(query)

            # Exact match
            if results["exact"]:
                print_concept(results["exact"])
            else:
                print("\n❌ No exact match found.")

            # Fuzzy matches
            print_fuzzy_results(results["fuzzy"])

            # Related concepts
            print_related_results(results["related"])

            # Keyword search
            print_keyword_results(results["keyword"])

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break

        except Exception as exc:
            print(f"\n❌ Error: {exc}")


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
