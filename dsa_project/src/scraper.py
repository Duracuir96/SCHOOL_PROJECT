"""
scraper.py
-----------
Hybrid web + LLM description generator for the DSA Knowledge Graph.

Order of operations for a given concept:
    1. Try to fetch a description from tutorial websites (e.g. GeeksforGeeks)
    2. If no suitable page is found:
         -> Try a local LLM (Ollama + phi3) to generate a short explanation
    3. If the LLM is not available or fails:
         -> Use a generic fallback sentence
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Dict, Iterable, Optional

import requests
from bs4 import BeautifulSoup

# --------------------------------------
# TRY IMPORT LOCAL OLLAMA
# --------------------------------------
try:
    import ollama  # type: ignore
    LLM_AVAILABLE = True
except Exception:
    ollama = None  # type: ignore
    LLM_AVAILABLE = False

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120 Safari/537.36"
}

REQUEST_TIMEOUT = 6
REQUEST_DELAY = 1.0
LLM_MODEL_NAME = "phi3"


# ---------------------------------------------------------------------------
# LLM FALLBACK
# ---------------------------------------------------------------------------
def llm_generate_description(concept_name: str, max_length: int = 400) -> Optional[str]:
    if not LLM_AVAILABLE:
        print(f"[LLM] Local model not available -> skipping LLM fallback for '{concept_name}'.")
        return None

    prompt = (
        "Explain the data structure or algorithm '" + concept_name + "' "
        "in 3–4 concise academic sentences. Include: definition, key idea, "
        "main operations, and typical use cases. No code."
    )

    try:
        print(f"[LLM] Generating fallback description for '{concept_name}'...")
        resp = ollama.generate(model=LLM_MODEL_NAME, prompt=prompt)  # type: ignore
        txt = resp.get("response", "").strip()
        if not txt:
            return None
        return txt[:max_length] + ("..." if len(txt) > max_length else "")
    except Exception as exc:
        print(f"[LLM] Error generating description: {exc}")
        return None


# ---------------------------------------------------------------------------
# SCRAPING HELPERS
# ---------------------------------------------------------------------------
def _slugify(name: str) -> str:
    s = name.strip().lower()
    for ch in [" ", "_", "/"]:
        s = s.replace(ch, "-")
    while "--" in s:
        s = s.replace("--", "-")
    return s


def _candidate_urls(concept_name: str):
    slug = _slugify(concept_name)
    patterns = [
        f"https://www.geeksforgeeks.org/{slug}-data-structure/",
        f"https://www.geeksforgeeks.org/{slug}-in-data-structure/",
        f"https://www.geeksforgeeks.org/{slug}-algorithm/",
        f"https://www.geeksforgeeks.org/{slug}/",
        f"https://www.geeksforgeeks.org/{slug}-in-c/",
        f"https://www.geeksforgeeks.org/{slug}-in-cpp/",
    ]
    for url in patterns:
        yield url


def _extract_paragraph(html: str, concept_name: str, max_length=400) -> Optional[str]:
    soup = BeautifulSoup(html, "html.parser")
    concept_lower = concept_name.lower()

    candidates = []
    for tag in soup.find_all(["p", "div"]):
        txt = tag.get_text(" ", strip=True)
        if len(txt) >= 80:
            candidates.append(txt)

    if not candidates:
        return None

    for c in candidates:
        if concept_lower in c.lower():
            return c[:max_length]

    return candidates[0][:max_length]


# ---------------------------------------------------------------------------
# PUBLIC API
# ---------------------------------------------------------------------------
def fetch_description(concept_name: str, max_length=400) -> str:
    print(f"\n[SCRAPER] Fetching description for: {concept_name}")

    for url in _candidate_urls(concept_name):
        try:
            print(f"[SCRAPER] Trying: {url}")
            r = requests.get(url, headers=DEFAULT_HEADERS, timeout=REQUEST_TIMEOUT)
            if r.status_code != 200:
                print(f"[SCRAPER] Status {r.status_code} for {url}")
                continue

            paragraph = _extract_paragraph(r.text, concept_name, max_length=max_length)
            if paragraph:
                print(f"[SCRAPER] ✔ FOUND description for '{concept_name}'")
                time.sleep(REQUEST_DELAY)
                return paragraph

        except Exception as exc:
            print(f"[SCRAPER] Error fetching {url}: {exc}")

    print(f"[SCRAPER] ❌ No web description -> trying LLM fallback for '{concept_name}'")
    llm_text = llm_generate_description(concept_name, max_length=max_length)
    if llm_text:
        print(f"[SCRAPER] ✔ LLM description OK for '{concept_name}'")
        return llm_text

    print(f"[SCRAPER] ⚠ Using generic fallback for '{concept_name}'")
    return f"A data structure or algorithm related to {concept_name}."
