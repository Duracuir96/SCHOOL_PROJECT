"""
search_engine.py
Search utilities for the DSA Knowledge Graph.
"""

from __future__ import annotations

import json
from pathlib import Path
from difflib import SequenceMatcher, get_close_matches
from typing import Any, Dict, List, Optional


# ---------------------- HELPERS ----------------------
def normalize_key(text: str) -> str:
    t = text.strip().lower()
    for ch in [" ", "-", "/"]:
        t = t.replace(ch, "_")
    while "__" in t:
        t = t.replace("__", "_")
    return t


def similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def snippet(text: str, q: str, w=60) -> str:
    if not text:
        return ""
    idx = text.lower().find(q.lower())
    if idx == -1:
        return text[: w * 2] + "..."
    start = max(0, idx - w)
    end = min(len(text), idx + len(q) + w)
    s = text[start:end]
    if start > 0:
        s = "..." + s
    if end < len(text):
        s = s + "..."
    return s


# ---------------------- SEARCH ENGINE ----------------------
class KnowledgeGraphSearch:
    def __init__(self, graph_file="data/knowledge_graph.json"):
        self.graph_file = Path(graph_file)
        if not self.graph_file.exists():
            raise FileNotFoundError(f"Graph not found: {self.graph_file}")

        with self.graph_file.open("r", encoding="utf-8") as f:
            self.graph: Dict[str, Dict[str, Any]] = json.load(f)

        self.concept_keys = list(self.graph.keys())
        self.concept_names = [self.graph[k].get("name", k) for k in self.concept_keys]

    def stats(self):
        return {
            "num_concepts": len(self.graph),
            "num_relations": sum(len(v.get("relations", [])) for v in self.graph.values()),
            "file": str(self.graph_file),
        }

    # ---------------------- EXACT ----------------------
    def exact_search(self, q: str):
        return self.graph.get(normalize_key(q))

    # ---------------------- FUZZY ----------------------
    def fuzzy_search(self, q: str, limit=5, cutoff=0.6):
        norm = normalize_key(q)
        res = {}
        close = get_close_matches(norm, self.concept_keys, n=limit, cutoff=cutoff)
        for k in close:
            d = self.graph[k]
            res[k] = {
                "name": d.get("name", k),
                "type": d.get("type", "unknown"),
                "match_score": similarity(norm, k),
            }
        return res

    # ---------------------- RELATION ----------------------
    def relation_search(self, rel: str):
        r = rel.lower()
        out = {}
        for k, v in self.graph.items():
            rels = [x.lower() for x in v.get("relations", [])]
            if r in rels:
                out[k] = {
                    "name": v.get("name", k),
                    "category": v.get("category", "unknown"),
                }
        return out

    # ---------------------- KEYWORD ----------------------
    def keyword_search(self, q: str):
        ql = q.lower()
        res = {}
        for k, v in self.graph.items():
            name = v.get("name", "")
            desc = v.get("description", "")
            if ql in (name + desc).lower():
                res[k] = {
                    "name": name,
                    "snippet": snippet(desc, q),
                }
        return res

    # ---------------------- COMBINED ----------------------
    def comprehensive_search(self, q: str):
        return {
            "exact": self.exact_search(q),
            "fuzzy": self.fuzzy_search(q),
            "related": self.relation_search(q),
            "keyword": self.keyword_search(q),
        }
