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
    {"title": "The Nightingale", "author": "Kristin Hannah"},
    {"title": "The Missing Pages", "author": "Alyson Richman"},
    {"title": "Braiding Sweetgrass", "author": "Robin Wall Kimmerer"},
]

TOP_N = 10

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


def fetch_google_books_description(title, author):
    try:
        resp = requests.get(
            "https://www.googleapis.com/books/v1/volumes",
            params={"q": f"intitle:{title} inauthor:{author}", "maxResults": 1},
            timeout=10,
        )
        items = resp.json().get("items", [])
        if not items:
            print(f"    [miss] no Google Books results for '{title}'")
            return ""
        info = items[0].get("volumeInfo", {})
        desc = info.get("description", "")
        if desc:
            print(
                f"    [hit]  Google Books description for '{title}' — {len(desc)} chars"
            )
        else:
            print(f"    [miss] no Google Books description for '{title}'")
        return desc
    except requests.RequestException as e:
        print(f"    [miss] Google Books request error for '{title}': {e}")
        return ""


def fetch_ol_metadata(title, author):
    resp = requests.get(
        "https://openlibrary.org/search.json",
        params={"title": title, "author": author, "limit": 1},
        timeout=10,
    )
    docs = resp.json().get("docs", [])
    if not docs:
        print(
            f"    [miss] no OL results for '{title}' by {author}, trying Google Books..."
        )
        desc = fetch_google_books_description(title, author)
        return desc or f"{title} by {author}", []

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
        else:
            print(
                f"    [miss] no description in work record for '{title}', trying Google Books..."
            )
            desc = fetch_google_books_description(title, author) or desc
        subjects = work.get("subjects", [])[:15]
    else:
        print(f"    [miss] no work key for '{title}'")

    # Fall back to search-result subjects if work endpoint returned none
    if not subjects:
        print(
            f"    [miss] no work subjects for '{title}', falling back to search subjects"
        )
        subjects = doc.get("subject", [])[:15]
    if not subjects:
        print(f"    [miss] no subjects found at all for '{title}'")

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


_GENERIC_SUBJECTS = {
    "fiction",
    "nonfiction",
    "literature",
    "prose literature",
    "biography",
}


def _is_usable_subject(s):
    s_lower = s.lower()
    if s_lower in _GENERIC_SUBJECTS:
        return False
    if s_lower.startswith("fiction /") or s_lower.startswith("nonfiction /"):
        return False
    if "fast (ocolc)" in s_lower or "(ocolc)" in s_lower:
        return False
    return True


def get_top_subjects(per_book=4):
    result = vectorstore._collection.get(include=["metadatas"])
    subjects = []
    for meta in result["metadatas"]:
        book_subjects = json.loads(meta.get("subjects", "[]"))
        usable = [s for s in book_subjects if _is_usable_subject(s)]
        subjects.extend(usable[:per_book])
    seen = set()
    deduped = []
    for s in subjects:
        if s not in seen:
            seen.add(s)
            deduped.append(s)
    return deduped[:10]


def fetch_candidates(subjects, per_author_limit=2):
    read_titles = {b["title"].lower() for b in READING_HISTORY}
    read_authors = {b["author"].lower() for b in READING_HISTORY}
    author_counts = Counter()
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
            authors_lower = [a.lower() for a in authors]
            if any(a in read_authors for a in authors_lower):
                continue
            if any(author_counts[a] >= per_author_limit for a in authors_lower):
                continue
            for a in authors_lower:
                author_counts[a] += 1
            candidates[key] = {"title": title, "authors": authors, "ol_key": key}
    return list(candidates.values())


def fetch_work_details(ol_key, title=""):
    """Returns (description, subjects) from the OL work record."""
    label = f"'{title}'" if title else ol_key
    try:
        resp = requests.get(f"https://openlibrary.org{ol_key}.json", timeout=10)
        if resp.status_code != 200:
            print(f"    [miss] {resp.status_code} fetching details for {label}")
            return "", []
        work = resp.json()
        raw = work.get("description", "")
        if isinstance(raw, dict):
            raw = raw.get("value", "")
        subjects = work.get("subjects", [])[:8]
        if not raw and not subjects:
            print(f"    [miss] no description or subjects for {label}")
        elif not raw:
            print(
                f"    [miss] no description for {label} (have {len(subjects)} subjects)"
            )
        else:
            print(f"    [hit]  {label} — {len(raw)} chars")
        return raw or "", subjects
    except requests.RequestException as e:
        print(f"    [miss] request error for {label}: {e}")
        return "", []


def rank_candidates(candidates, description_fetch_limit=40):
    print(f"Fetching descriptions for up to {description_fetch_limit} candidates...")
    for book in candidates[:description_fetch_limit]:
        if book.get("ol_key") and "description" not in book:
            desc, subjects = fetch_work_details(book["ol_key"], title=book["title"])
            book["description"] = desc
            book["work_subjects"] = subjects
            time.sleep(0.4)

    scored = []
    for book in candidates:
        desc = book.get("description", "")
        title_author = f"{book['title']} by {', '.join(book['authors'])}"
        if len(desc) > 80:
            query = desc
        elif book.get("work_subjects"):
            query = f"{title_author}. Topics: {', '.join(book['work_subjects'][:5])}"
        else:
            query = title_author
        results = vectorstore.similarity_search_with_score(query, k=1)
        if results:
            score = results[0][1]  # L2 distance — lower = more similar
            scored.append((score, book))
    scored.sort(key=lambda x: x[0])
    return [book for _, book in scored]


def deduplicate_by_author(ranked, max_per_author=1):
    seen = Counter()
    result = []
    for book in ranked:
        authors_lower = [a.lower() for a in book["authors"]]
        if all(seen[a] < max_per_author for a in authors_lower):
            for a in authors_lower:
                seen[a] += 1
            result.append(book)
    return result


def rerank_with_claude(candidates, pool_size=20):
    history = ", ".join(f"{b['title']} by {b['author']}" for b in READING_HISTORY)
    pool = candidates[:pool_size]

    lines = []
    for i, book in enumerate(pool):
        authors = ", ".join(book["authors"]) or "unknown"
        desc = book.get("description", "")
        subjects = book.get("work_subjects", [])
        entry = f"{i + 1}. {book['title']} by {authors}"
        if desc:
            entry += f" — {desc[:250]}"
        elif subjects:
            entry += f" — Topics: {', '.join(subjects[:4])}"
        lines.append(entry)

    msg = (
        f"A reader has enjoyed: {history}.\n\n"
        f"Below are {len(pool)} candidate books. Rank them best-to-worst for this reader. "
        f"Exclude academic texts, children's books, poetry collections, and anything clearly off-genre. "
        f"Return ONLY a JSON array of 1-based indices in ranked order, e.g. [3, 7, 1, ...]. No explanation.\n\n"
        + "\n".join(lines)
    )

    response = llm.invoke(msg).content.strip()
    try:
        start, end = response.index("["), response.rindex("]") + 1
        indices = json.loads(response[start:end])
        reranked = []
        seen_idx = set()
        for idx in indices:
            i = int(idx) - 1
            if 0 <= i < len(pool) and i not in seen_idx:
                seen_idx.add(i)
                reranked.append(pool[i])
        return reranked
    except (ValueError, KeyError, json.JSONDecodeError):
        print("  [warn] Claude rerank parse failed, falling back to embedding order")
        return pool


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
    ranked = deduplicate_by_author(ranked)

    print("Reranking top candidates with Claude...")
    ranked = rerank_with_claude(ranked)

    print(f"\n--- Top {TOP_N} Recommendations ---\n")
    for book in ranked[:TOP_N]:
        authors = ", ".join(book["authors"]) or "unknown"
        print(f"{book['title']} by {authors}")
        print(f"  {explain(book)}")
        print(f"  NYPL: {nypl_link(book['title'])}\n")


if __name__ == "__main__":
    main()
