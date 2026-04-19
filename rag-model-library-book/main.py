import json
import os
import time
from collections import Counter

import requests
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

load_dotenv()

# --- Your reading history — edit this list ---
READING_HISTORY = [
    {"title": "The Name of the Wind", "author": "Patrick Rothfuss"},
    {"title": "Dune", "author": "Frank Herbert"},
    {"title": "The Left Hand of Darkness", "author": "Ursula K. Le Guin"},
]

TOP_N = 5

embedder = HuggingFaceEmbeddings(model_name=os.environ["HF_EMBEDDING_MODEL"])
llm = ChatAnthropic(
    model=os.environ["ANTHROPIC_MODEL"],
    api_key=os.environ["ANTHROPIC_API_KEY"],
)
vectorstore = Chroma(
    collection_name="reading_history",
    persist_directory="./chroma_db",
    embedding_function=embedder,
)


def fetch_ol_metadata(title, author):
    resp = requests.get(
        "https://openlibrary.org/search.json",
        params={"title": title, "author": author, "limit": 1},
        timeout=10,
    )
    docs = resp.json().get("docs", [])
    if not docs:
        return f"{title} by {author}", []

    doc = docs[0]
    work_key = doc.get("key", "")

    desc = f"{title} by {author}"
    subjects = []
    if work_key:
        work = requests.get(
            f"https://openlibrary.org{work_key}.json", timeout=10
        ).json()
        raw = work.get("description", "")
        if isinstance(raw, dict):
            raw = raw.get("value", "")
        if raw:
            desc = raw
        subjects = work.get("subjects", [])[:15]

    print(f"    subjects found: {subjects[:3]}")
    return desc, subjects


def index_reading_history():
    if vectorstore._collection.count() > 0:
        print(
            f"Using existing index ({vectorstore._collection.count()} books). Delete ./chroma_db to re-index."
        )
        return

    docs = []
    for book in READING_HISTORY:
        print(f"  Fetching: {book['title']}...")
        desc, subjects = fetch_ol_metadata(book["title"], book["author"])
        time.sleep(0.5)
        docs.append(
            Document(
                page_content=desc,
                metadata={
                    "title": book["title"],
                    "author": book["author"],
                    "subjects": json.dumps(subjects),
                },
            )
        )

    vectorstore.add_documents(docs)
    print(f"Indexed {len(docs)} books.\n")


def get_top_subjects():
    result = vectorstore._collection.get(include=["metadatas"])
    subjects = []
    for meta in result["metadatas"]:
        subjects.extend(json.loads(meta.get("subjects", "[]")))
    return [s for s, _ in Counter(subjects).most_common(10)]


def fetch_candidates(subjects):
    read_titles = {b["title"].lower() for b in READING_HISTORY}
    candidates = {}
    for subject in subjects[:6]:
        slug = subject.lower().replace(" ", "_").replace(",", "")
        resp = requests.get(
            f"https://openlibrary.org/subjects/{slug}.json",
            params={"limit": 20},
            timeout=10,
        )
        time.sleep(0.5)
        if resp.status_code != 200:
            continue
        for work in resp.json().get("works", []):
            title = work.get("title", "")
            if title.lower() in read_titles:
                continue
            key = work.get("key")
            authors = [a.get("name", "") for a in work.get("authors", [])]
            candidates[key] = {"title": title, "authors": authors}
    return list(candidates.values())


def rank_candidates(candidates):
    scored = []
    for book in candidates:
        query = f"{book['title']} by {', '.join(book['authors'])}"
        results = vectorstore.similarity_search_with_score(query, k=1)
        if results:
            score = results[0][1]  # L2 distance — lower = more similar
            scored.append((score, book))
    scored.sort(key=lambda x: x[0])
    return [book for _, book in scored]


def explain(book):
    history = ", ".join(f"{b['title']} by {b['author']}" for b in READING_HISTORY)
    authors = ", ".join(book["authors"]) or "unknown"
    msg = (
        f"Someone has read: {history}. "
        f'In 2 sentences, explain why they might enjoy "{book["title"]}" by {authors}.'
    )
    return llm.invoke(msg).content


def nypl_link(title):
    from urllib.parse import quote

    return f"https://borrow.nypl.org/search?query={quote(title)}&searchType=everything"


def main():
    print("Indexing reading history...")
    index_reading_history()

    subjects = get_top_subjects()
    print(f"Top subjects: {subjects[:5]}")

    print("\nFetching candidates from Open Library...")
    candidates = fetch_candidates(subjects)
    print(f"Found {len(candidates)} candidates. Ranking by similarity...")

    ranked = rank_candidates(candidates)

    print(f"\n--- Top {TOP_N} Recommendations ---\n")
    for book in ranked[:TOP_N]:
        authors = ", ".join(book["authors"]) or "unknown"
        print(f"{book['title']} by {authors}")
        print(f"  {explain(book)}")
        print(f"  NYPL: {nypl_link(book['title'])}\n")


if __name__ == "__main__":
    main()
