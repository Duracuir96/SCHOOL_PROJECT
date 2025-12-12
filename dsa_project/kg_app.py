# kg_app.py
"""
DSA Knowledge Graph – Search & Visualization App
------------------------------------------------

This Streamlit application demonstrates the main deliverables
of the “DSA Knowledge Graph Construction and Search” project:

    1. Construction of a DSA Knowledge Graph (stored in JSON)
    2. Custom search algorithms:
         - exact search
         - fuzzy search
         - relation-based search
         - keyword search
    3. Graph visualization (global mindmap + local neighborhood)
    4. Natural-language explanations based ONLY on the KG content

Internal logic of the engines is NOT modified:
    - KnowledgeGraphSearch
    - DsaTutorEngine
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

import streamlit as st
from streamlit.components.v1 import html

from src.tutor_engine import DsaTutorEngine          # explanation engine (unchanged)
from src.search_engine import KnowledgeGraphSearch   # search engine (unchanged)

from pyvis.network import Network
import tempfile


# =====================================================================
# STREAMLIT CONFIG
# =====================================================================
st.set_page_config(
    page_title="DSA Knowledge Graph – Search & Visualization",
    layout="wide",
)


# =====================================================================
# LOAD ENGINES / KNOWLEDGE GRAPH
# =====================================================================
@st.cache_resource
def load_engines():
    """
    Charge le fichier du graphe de connaissances et initialise les moteurs.
    """
    import os
    from pathlib import Path

    # --- DÉBUT DE LA CORRECTION ---
    # Essayer plusieurs emplacements possibles
    emplacements_possibles = [
        Path("data/knowledge_graph.json"),           # Si data/ est à la racine
        Path("dsa_project/data/knowledge_graph.json"), # Si data/ est dans dsa_project/
        Path("../data/knowledge_graph.json"),        # Ancien chemin (pour compatibilité)
        Path(__file__).parent / "data" / "knowledge_graph.json", # Chemin précis basé sur kg_app.py
    ]

    graph_path = None
    for chemin in emplacements_possibles:
        if chemin.exists():
            graph_path = chemin
            st.sidebar.success(f"✅ Fichier trouvé : {chemin}")
            break

    if graph_path is None:
        # Pour le débogage : lister les fichiers disponibles
        st.error("❌ Impossible de trouver 'knowledge_graph.json'.")
        st.write("📁 Contenu du dossier courant (pour débogage) :")
        st.write(list(Path(".").rglob("*")))  # Montre tous les fichiers
        raise FileNotFoundError("Fichier knowledge_graph.json introuvable. Voir la structure ci-dessus.")

    tutor = DsaTutorEngine(str(graph_path))
    search_engine = KnowledgeGraphSearch(str(graph_path))
    kg: Dict[str, Dict[str, Any]] = tutor.kg

    return tutor, search_engine, kg, graph_path


# =====================================================================
# GLOBAL STATIC MINDMAP (PROF-FRIENDLY OVERVIEW)
# =====================================================================
def draw_static_mindmap():
    """
    A clean, static mindmap that illustrates the high-level
    structure of the DSA Knowledge Graph.

    Nodes are grouped visually:
        - Blue  = Data Structures
        - Orange = Algorithms
        - Purple = Graph Algorithms
    All nodes are connected to the central “Knowledge Graph” hub
    with simple lines so the evaluator can immediately see that
    everything belongs to the same DSA knowledge space.
    """

    mindmap_html = """
    <style>
        .mindmap-container {
            position: relative;
            width: 750px;
            height: 750px;
            margin-left: auto;
            margin-right: auto;
        }
        .mindmap-center {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #2CA6A4;
            color: white;
            padding: 22px 32px;
            border-radius: 100%;
            font-size: 22px;
            font-weight: bold;
            text-align: center;
            box-shadow: 0px 0px 10px #444;
        }
        .mindmap-node {
            position: absolute;
            color: white;
            padding: 12px 18px;
            border-radius: 999px;
            text-align: center;
            font-size: 14px;
            min-width: 120px;
            transform: translate(-50%, -50%);
            box-shadow: 0px 3px 8px rgba(0,0,0,0.3);
            white-space: nowrap;
        }
        .ds-node {
            background: #1E3A8A;  /* Data structures: blue */
        }
        .algo-node {
            background: #EA580C;  /* Algorithms: orange */
        }
        .graphalgo-node {
            background: #7C3AED;  /* Graph algorithms: purple */
        }
        .legend-box {
            margin-top: 10px;
            font-size: 13px;
        }
        .legend-color {
            display: inline-block;
            width: 14px;
            height: 14px;
            border-radius: 3px;
            margin-right: 6px;
        }
    </style>

    <div class="mindmap-container">
        <!-- SVG LINES (connections) -->
        <svg width="100%" height="100%" style="position:absolute; top:0; left:0;">
            <!-- center: (50%, 50%) -->

            <!-- Data structures -->
            <line x1="50%" y1="50%" x2="18%" y2="30%" stroke="#1E3A8A" stroke-width="2"/>
            <line x1="50%" y1="50%" x2="15%" y2="50%" stroke="#1E3A8A" stroke-width="2"/>
            <line x1="50%" y1="50%" x2="20%" y2="70%" stroke="#1E3A8A" stroke-width="2"/>
            <line x1="50%" y1="50%" x2="35%" y2="85%" stroke="#1E3A8A" stroke-width="2"/>
            <line x1="50%" y1="50%" x2="80%" y2="30%" stroke="#1E3A8A" stroke-width="2"/>
            <line x1="50%" y1="50%" x2="85%" y2="60%" stroke="#1E3A8A" stroke-width="2"/>

            <!-- Algorithms -->
            <line x1="50%" y1="50%" x2="35%" y2="15%" stroke="#EA580C" stroke-width="2"/>
            <line x1="50%" y1="50%" x2="65%" y2="10%" stroke="#EA580C" stroke-width="2"/>
            <line x1="50%" y1="50%" x2="65%" y2="80%" stroke="#EA580C" stroke-width="2"/>
            <line x1="50%" y1="50%" x2="50%" y2="90%" stroke="#EA580C" stroke-width="2"/>

            <!-- Graph Algorithms -->
            <line x1="50%" y1="50%" x2="30%" y2="35%" stroke="#7C3AED" stroke-width="2"/>
            <line x1="50%" y1="50%" x2="30%" y2="60%" stroke="#7C3AED" stroke-width="2"/>
        </svg>

        <!-- CENTER NODE -->
        <div class="mindmap-center">
            DSA<br/>Knowledge Graph
        </div>

        <!-- DATA STRUCTURES (blue) -->
        <div class="mindmap-node ds-node" style="top:30%; left:18%;">Array</div>
        <div class="mindmap-node ds-node" style="top:50%; left:15%;">Linked List</div>
        <div class="mindmap-node ds-node" style="top:70%; left:20%;">Stack</div>
        <div class="mindmap-node ds-node" style="top:85%; left:35%;">Queue</div>
        <div class="mindmap-node ds-node" style="top:30%; left:80%;">Tree</div>
        <div class="mindmap-node ds-node" style="top:60%; left:85%;">Graph</div>

        <!-- ALGORITHMS (orange) -->
        <div class="mindmap-node algo-node" style="top:15%; left:35%;">Recursion</div>
        <div class="mindmap-node algo-node" style="top:10%; left:65%;">Bubble Sort</div>
        <div class="mindmap-node algo-node" style="top:80%; left:65%;">Quick Sort</div>
        <div class="mindmap-node algo-node" style="top:90%; left:50%;">Merge Sort</div>

        <!-- GRAPH ALGORITHMS (purple) -->
        <div class="mindmap-node graphalgo-node" style="top:35%; left:30%;">BFS</div>
        <div class="mindmap-node graphalgo-node" style="top:60%; left:30%;">DFS</div>
    </div>

    <div class="legend-box">
        <span class="legend-color" style="background:#1E3A8A;"></span>
        <strong>Blue:</strong> core data structures (Array, Linked List, Stack, Queue, Tree, Graph)<br/>
        <span class="legend-color" style="background:#EA580C;"></span>
        <strong>Orange:</strong> classic algorithms (Recursion, Bubble / Quick / Merge Sort)<br/>
        <span class="legend-color" style="background:#7C3AED;"></span>
        <strong>Purple:</strong> graph traversal algorithms (BFS, DFS)
    </div>
    """

    html(mindmap_html, height=800)


# =====================================================================
# LOCAL NEIGHBORHOOD GRAPH (PyVis, SEARCH-DRIVEN)
# =====================================================================
def build_concept_graph(concept_key: str, kg, search_engine) -> str:
    """
    Draw a neighborhood graph around the selected concept using PyVis.

    - Center node  = selected concept (orange)
    - Blue boxes   = relation tags (e.g. "linear_structure", "ordering")
    - Green nodes  = other KG concepts sharing the same relation
    """
    concept = kg.get(concept_key)
    if not concept:
        raise ValueError(f"Concept '{concept_key}' does not exist in the KG.")

    net = Network(
        height="600px",
        width="100%",
        bgcolor="#0e1117",
        font_color="white",
        notebook=False,
    )
    net.barnes_hut()

    # Central node = the concept
    central_label = concept.get("name", concept_key)
    net.add_node(
        concept_key,
        label=central_label,
        size=28,
        color="#ffb000",  # orange
    )

    relations = concept.get("relations", []) or []
    MAX_NEIGHBORS = 6

    for rel in relations:
        rel_key = f"rel::{rel}"

        # Relation node
        net.add_node(
            rel_key,
            label=rel,
            shape="box",
            color="#00b5ff",  # blue
        )
        net.add_edge(concept_key, rel_key)

        # Concepts connected via the same relation tag
        related = search_engine.relation_search(rel)
        count = 0

        for key, info in related.items():
            if key == concept_key:
                continue
            if count >= MAX_NEIGHBORS:
                break

            net.add_node(
                key,
                label=info.get("name", key),
                color="#7cff7c",  # green
                size=18,
            )
            net.add_edge(rel_key, key)
            count += 1

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    net.write_html(tmp.name)
    return tmp.name


# =====================================================================
# MAIN STREAMLIT APP
# =====================================================================
def main():

    st.title("📚 DSA Knowledge Graph – Search & Visualization")

    # =============== GLOBAL OVERVIEW (STATIC MINDMAP) ===============
    st.subheader("🌐 Global Knowledge Graph Overview")
    st.write(
        " 您好老师欢迎， Welcome! "
                "  "
        "📌 This overview is a simplified mindmap. "
    "It does not show all nodes or relations from the full Knowledge Graph. "
    "Its purpose is to provide an intuitive, easy-to-read introduction before "
    "exploring the detailed PyVis graph."
    )
    draw_static_mindmap()
    st.markdown("---")

    # =============== PROJECT DESCRIPTION ===============
    st.markdown(
        """
### 📘 Project Demonstration

This application illustrates the core requirements of the assignment:

- **Knowledge Graph construction** – the graph is stored in JSON format in  
  `data/knowledge_graph.json`.
- **Search algorithms** – we implement exact search, fuzzy search,  
  relation-based search and keyword search over the graph.
- **Explanation engine** – natural-language answers are generated from the  
  metadata of each concept in the KG (no external data).
- **Graph visualization** – local neighborhoods of the graph are rendered
  with PyVis for interactive exploration.
"""
    )

    # =============== LOAD ENGINES ===============
    try:
        tutor, search_engine, kg, graph_path = load_engines()
    except Exception as e:
        st.error("❌ Cannot load knowledge_graph.json")
        st.code(str(e))
        return

    # ==================== SIDEBAR ====================
    with st.sidebar:
        st.header("⚙️ Search Options")
        st.markdown(f"**Loaded KG file:** `{graph_path}`")

        stats = search_engine.stats()
        st.markdown(
            f"""
- Concepts in KG: **{stats['num_concepts']}**
- Relation tags: **{stats['num_relations']}**
            """
        )

        mode = st.radio(
            "Search / Explanation Mode",
            ["Concept explanation (natural language)", "Structured search"],
        )

        user_query = st.text_input(
            "🔍 Query or concept",
            value="Explain binary search",
            help="Examples: 'Explain stack', 'binary search', 'graph traversal', 'queue'…",
        )

    # ==================== MAIN LAYOUT ====================
    left, right = st.columns([3, 2])

    current_concept_key = None
    tutor_result: Dict[str, Any] | None = None
    search_results: Dict[str, Any] | None = None

    # ==================== HANDLE SEARCH ONLY (NO BROWSE) ====================
    if user_query.strip():
        if mode.startswith("Concept explanation"):
            # Natural language explanation based on KG
            tutor_result = tutor.answer(user_query)
            current_concept_key = tutor_result.get("matched_key")

        else:
            # Structured search over the knowledge graph
            search_results = search_engine.comprehensive_search(user_query)
            exact_obj = search_results.get("exact")

            if exact_obj:
                # We locate the KG key using the unique ID stored in the JSON
                exact_id = exact_obj.get("id")
                for key, node in kg.items():
                    if node.get("id") == exact_id:
                        current_concept_key = key
                        break

    # ==================== LEFT COLUMN ====================
    with left:
        if mode.startswith("Concept explanation"):
            st.subheader("🧠 Concept Explanation (from the Knowledge Graph)")

            if not tutor_result:
                st.info("Type a query (e.g. 'Explain stack', 'Explain BFS') to get an explanation.")
            else:
                st.markdown(f"**Query:** `{tutor_result['query']}`")
                st.markdown(f"**Matched via:** `{tutor_result['match_source']}`")

                if tutor_result.get("matched_key"):
                    st.markdown(f"**Internal KG key:** `{tutor_result['matched_key']}`")

                st.markdown("---")
                st.markdown(tutor_result["answer_markdown"])

        else:
            st.subheader("🔍 Structured Search Results")

            if not search_results:
                st.info("Enter a query to search the Knowledge Graph.")
            else:
                exact = search_results.get("exact")
                fuzzy = search_results.get("fuzzy") or {}
                related = search_results.get("related") or {}
                keyword = search_results.get("keyword") or {}

                st.markdown("### 🎯 Exact match")
                if exact:
                    st.json(exact)
                else:
                    st.write("No exact match found.")

                st.markdown("### 🤔 Fuzzy matches")
                st.write(fuzzy or "None")

                st.markdown("### 🔗 Related concepts (by relation tags)")
                st.write(related or "None")

                st.markdown("### 🔍 Keyword hits (in descriptions / use cases)")
                st.write(keyword or "None")

    # ==================== RIGHT COLUMN: LOCAL GRAPH ====================
    with right:
        st.subheader("📈 Local Neighborhood Graph (PyVis)")

        if not current_concept_key:
            st.info(
                "After you type a query that matches a concept in the KG, "
                "a local neighborhood graph will be displayed here."
            )
        else:
            st.markdown(f"**Current concept key in KG:** `{current_concept_key}`")

            try:
                html_file = build_concept_graph(current_concept_key, kg, search_engine)
                with open(html_file, "r", encoding="utf-8") as f:
                    html(f.read(), height=600)
            except Exception as e:
                st.error(f"Graph rendering error: {e}")

            # Clear explanation for the teacher about how to read the PyVis graph
            st.markdown(
                """
**How to read this graph:**

- The **central orange node** is the concept that was matched by the search  
  (for example: `Stack`, `Binary Search`, `Graph`, etc.).
- The **blue box nodes** correspond to **relation tags** stored in the Knowledge Graph  
  (e.g. `linear_structure`, `ordering`, `graph_traversal`).
- The **green nodes** are **other DSA concepts** that share the same relation tag.
- The **edges** show “is related via this relation tag”.  

This means the PyVis view is a *local neighborhood* around the selected concept,
showing **how it is connected to other concepts** according to the JSON-based
knowledge graph.
                """
            )


if __name__ == "__main__":
    main()

