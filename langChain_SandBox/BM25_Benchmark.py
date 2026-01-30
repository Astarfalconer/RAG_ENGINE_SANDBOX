import time
import statistics
import nltk
from nltk.tokenize import word_tokenize
from langchain_community.retrievers import BM25Retriever
from rank_bm25 import BM25Okapi
import bm25s  
from RagIntake import docs

# If needed once:
nltk.download("punkt_tab")

def bench(fn, runs=50):
    times = []
    last = None
    for _ in range(runs):
        t0 = time.perf_counter()
        last = fn()
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000)  # ms
    return {
        "runs": runs,
        "mean_ms": statistics.mean(times),
        "p50_ms": statistics.median(times),
        "p95_ms": sorted(times)[int(0.95 * (runs - 1))],
        "last": last,
    }

def contains_keywords(docs, keywords=("point scoring", "scoring", "04 points")):
    joined = "\n".join([d.page_content.lower() for d in docs])
    return {k: (k in joined) for k in keywords}

# --- Shared corpus ---
texts = [d.page_content for d in docs]
tokenized_corpus = [word_tokenize(t) for t in texts]

query = "What are the IBJJF rules for scoring points in a match?"
k = 5
tokenized_query = word_tokenize(query)

# --- A) LangChain BM25Retriever ---
lc_bm25 = BM25Retriever.from_documents(docs, preprocess_func=word_tokenize)
lc_bm25.k = k

def run_langchain():
    return lc_bm25.invoke(query)  # List[Document]

# --- B) rank-bm25 direct ---
rb_bm25 = BM25Okapi(tokenized_corpus)

def run_rankbm25():
    scores = rb_bm25.get_scores(tokenized_query)
    top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    return [docs[i] for i in top_idx]  # List[Document]

# --- C) bm25s (BM25S) ---
# Build BM25S index once
bm25s_corpus_tokens = [word_tokenize(t) for t in texts]

# bm25s expects a list of token lists; we build an index object and index the corpus.
bm25s_index = bm25s.BM25()
bm25s_index.index(bm25s_corpus_tokens)

def run_bm25s():
    q = word_tokenize(query)          # q is List[str]
    scores, indices = bm25s_index.retrieve([q], k=k)  # <- batch of 1 query
    # scores/indices are now nested (one entry per query)
    indices = indices[0]
    return [docs[int(i)] for i in indices]




# --- Run benches ---
lc_stats = bench(run_langchain, runs=50)
rb_stats = bench(run_rankbm25, runs=50)
bs_stats = bench(run_bm25s, runs=50)

print("\n=== BM25 Bench (ms) ===")
print(f"LangChain BM25Retriever: mean={lc_stats['mean_ms']:.3f} p50={lc_stats['p50_ms']:.3f} p95={lc_stats['p95_ms']:.3f}")
print(f"rank-bm25 BM25Okapi   : mean={rb_stats['mean_ms']:.3f} p50={rb_stats['p50_ms']:.3f} p95={rb_stats['p95_ms']:.3f}")
print(f"bm25s BM25            : mean={bs_stats['mean_ms']:.3f} p50={bs_stats['p50_ms']:.3f} p95={bs_stats['p95_ms']:.3f}")

print("\n=== Quality check (keyword presence in top-k) ===")
print("LangChain:", contains_keywords(lc_stats["last"]))
print("rank-bm25:", contains_keywords(rb_stats["last"]))
print("bm25s    :", contains_keywords(bs_stats["last"]))

# Optional: print top result page numbers
def pages(ds):
    return [d.metadata.get("page") for d in ds]

print("\nTop-k pages:")
print("LangChain:", pages(lc_stats["last"]))
print("rank-bm25:", pages(rb_stats["last"]))
print("bm25s    :", pages(bs_stats["last"]))

