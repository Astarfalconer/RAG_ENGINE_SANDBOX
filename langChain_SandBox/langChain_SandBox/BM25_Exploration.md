# BM25 & Hybrid Retrieval – Initial Exploration 

## Purpose

Investigating whether adding lexical BM25 retrieval alongside vector similarity search improves retrieval quality for rule-heavy and technical documents.

---

## What I Implemented

- Added BM25 retrieval using `langchain_community.retrievers.BM25Retriever`
- Built BM25 index from the same filtered document chunks used for embeddings
- Implemented parallel retrieval:
  - Vector similarity search (k = 5)
  - BM25 search (k = 5)
- Implemented merge and deduplication of results from both retrievers

---

## Dependencies / Libraries Used

- `langchain`
- `langchain-community`
- `nltk`
- Existing vector store + embedding stack (already in project)

---

## Dataset / Scale

- Corpus size: ~70 chunks  
- Domain: PDF rules document (IBJJF rules)

---

## Observations

**Test query:**  
“What are the IBJJF rules for scoring points in a match?”

- BM25 reliably surfaces sections with explicit headings such as **“POINT SCORING”**
- Vector search surfaces semantically related passages
- Hybrid merge contains more relevant scoring-related chunks than vector-only retrieval
- BM25 is particularly useful for tables and structured rule sections

---

## Performance (Informal)

Local laptop testing:

- BM25 retrieval appears effectively instantaneous (few ms) at this scale
- No noticeable slowdown compared to vector similarity search

---

## Current Limitations

- No reranking implemented yet
- No query rewriting implemented yet
- Simple merge strategy (no weighting or scoring fusion)

---

## BM25 Open-Source Comparison (A/B/C)

Tested three BM25 implementations locally:

- A) `langchain_community.retrievers.BM25Retriever`
- B) `rank-bm25` (BM25Okapi)
- C) `bm25s` (BM25S)

**Benchmark setup**

- Corpus size: ~70 chunks  
- Query: “What are the IBJJF rules for scoring points in a match?”  
- Top-k: 5  
- 50 runs each  
- Wall-clock timing (ms)

**Latency**

- LangChain BM25Retriever: mean 0.151 ms, p50 0.128 ms, p95 0.274 ms  
- rank-bm25 BM25Okapi: mean 0.096 ms, p50 0.085 ms, p95 0.101 ms  
- bm25s BM25: mean 0.266 ms, p50 0.224 ms, p95 0.402 ms  

**Quality / Result alignment**

- LangChain and rank-bm25 returned identical top-k pages: `[5, 14, 28, 27, 22]`  
  - Keyword presence in top-k included “point scoring” and “scoring”
- bm25s returned different pages: `[3, 3, 2, 2, 2]`  
  - Keyword presence checks were false for “point scoring” and “scoring”

**Takeaway**

- `rank-bm25` is currently the best option in this sandbox (fastest + correct retrieval)
- LangChain BM25Retriever is also viable (same retrieval output, slightly higher overhead, simpler integration)
- `bm25s` is not returning relevant sections in current setup and is slower; would require further investigation/configuration before use

---

## Next Steps

- Add query rewriting step before retrieval  
- Compare latency between rewrite approaches  

---

## External Query Rewrite API Pricing (Token-based)

| API Provider | Model / Tier | Input Cost | Output Cost | Notes |
|-------------|-------------|------------|-------------|------|
| OpenAI API | GPT-4.1 (example) | ~$3.00 / 1M tokens | ~$12.00 / 1M tokens | https://openai.com/api/pricing |
| Anthropic Claude | Claude Sonnet 4.5 | ~$3.00 / 1M tokens | ~$15.00 / 1M tokens | https://platform.claude.com/docs/en/about-claude/pricing |
| Anthropic Claude | Claude Opus 4.5 | ~$5.00 / 1M tokens | ~$25.00 / 1M tokens | https://platform.claude.com/docs/en/about-claude/pricing |
| Cohere API | Command R | ~$0.15 / 1M tokens | ~$0.60 / 1M tokens | https://cohere.com/pricing |
| Cohere API | Command A | ~$2.50 / 1M tokens | ~$10.00 / 1M tokens | https://cohere.com/pricing |
| Cohere API | Command R7B | ~$0.0375 / 1M tokens | ~$0.15 / 1M tokens | https://cohere.com/pricing |

**Note:** These services charge per tokens processed, not per GB of indexed data. Actual cost scales with query and rewrite length.

## Test 1: Query Rewriting & Hybrid Retrieval

### Test Query & Rewrite:
- **Original Query:**  
  "What are the IBJJF rules for scoring points in a match?"

- **Rewritten Query (via simple rewrite method):**  
  "What are the specific IBJJF scoring rules for awarding points during a Brazilian Jiu-Jitsu match?"

---

### Results after Hybrid Retrieval (Merged Documents):

- **Number of Documents Merged:**  
  10 documents retrieved (top-k)

#### Merged Documents (Sample):
- **Source Page 5:**  
  Contains detailed rules about scoring points, moving out of bounds, and submissions.

- **Source Page 14:**  
  Focuses on point-scoring and penalties, with structured sections for each rule type.

---

### Key Observations:
- The **rewritten query surfaced** a **wider scope of relevant documents**, including ones that focus on different aspects of the rules, aligning with a broader user query.
- **Documents retrieved** included scoring points and penalties, which seemed more aligned with the rewrite.
- **BM25 and hybrid search** effectively highlighted **sections with clear headings and structure**, as expected.

---

---


## Test 2: Query Rewriting & Hybrid Retrieval

### Original Query:
- **"Who can use swords in this game?"**

### Rewritten Query (via simple rewrite method):
- **"Which characters or classes in this game have the ability to wield swords?"**

---

### Results after Hybrid Retrieval (Merged Documents):

- **Number of Documents Merged:**  
  5 documents retrieved (top-k)

#### Merged Documents (Sample):
- **Source Page 5:**  
  - Contains personality traits, ideals, bonds, flaws, and backstory information.
  - Mentions specific character background and class traits relevant to sword usage.

- **Source Page 14:**  
  - Discusses additional gameplay aspects, including character abilities and actions during the game.

---

### Key Observations:
- The **rewritten query surfaced** **more targeted documents** focused on character abilities, which align better with the revised query.
- **Hybrid retrieval** (BM25 + vector search) helped surface **a broader set of related documents**, including character classes and their corresponding abilities.

---

### Next Steps for Refinement:
- **Query Rewriting:** Investigate whether **LLM-based query rewriting** (via external APIs like OpenAI or Cohere) leads to further improvements in retrieval quality.
- **Evaluate More Complex Queries:** Test more **complex query rewrites** to understand their effects on document retrieval and precision/recall.


### Side-by-side test:

- **Original query:**
"Who can use swords in this game?"
→ Returned general introduction page (no weapon/class info)

- **Rewritten query:**
"Which characters or classes have the ability to wield swords in this game?"
→ Returned Fighter class section containing explicit sword usage

**Conclusion:**
Query rewriting significantly improved retrieval precision and reduced noise.
