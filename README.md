# RAG Sandbox

A lightweight sandbox for building and understanding a **Retrieval-Augmented Generation (RAG)** pipeline using Python, LangChain, and FAISS.

This project is intentionally minimal and learning-focused. The goal is to understand how each layer of a RAG system works before introducing higher-level abstractions.

---

## 🎯 Purpose

* Learn how documents become searchable vectors
* Make retrieval predictable and debuggable
* Understand how metadata flows through a RAG system
* Establish a solid foundation for adding memory and agent behavior later

---

## 🧠 Conceptual Pipeline

```
Documents (PDF / Text)
        ↓
Load
        ↓
Chunk
        ↓
Chunk Objects (with metadata)
        ↓
LangChain Documents
        ↓
Embeddings
        ↓
FAISS Vector Store
        ↓
Similarity Search
        ↓
Retrieved Chunks
        ↓
LLM Prompt
        ↓
Answer
```

---

## 📁 Project Structure

```
rag_sandbox/
│
├─ ExampleData/            # Sample PDFs
│
├─ RagIntake.py            # Loads PDFs, chunks text, filters junk, creates Chunk objects
├─ ChunkClass.py           # Dataclass definition for Chunk
├─ VectorStore.py          # Builds FAISS index and runs similarity searches
│
├─ requirements.txt
└─ README.md
```

---

## 📦 Chunk Object

Each chunk is represented internally as a dataclass:

* `chunk_id`  – unique identifier
* `content`   – chunk text
* `page`      – page number
* `source`    – source file

Chunks are converted into LangChain `Document` objects before being inserted into FAISS.

---

## 📚 Metadata

Every stored vector contains metadata:

```
{
  "chunk_id": "...",
  "page": 12,
  "source": "ExampleData/file.pdf"
}
```

This enables:

* Tracing where an answer came from
* Debugging retrieval quality
* Adding citations later

---

## 🔍 Retrieval

FAISS is used with **L2 distance**.

Two common calls:

* `similarity_search()` → returns Documents
* `similarity_search_with_score()` → returns (Document, distance)

Smaller distance = more similar.

---

## ✅ Thresholding

To avoid hallucinations:

1. Retrieve top-k results (e.g., k=5)
2. Inspect best distance
3. If best distance > threshold → return "Information not found"

Threshold is determined empirically by testing good vs bad queries.

---

## 🧪 Basic Workflow

1. Place PDFs in `ExampleData/`
2. Run `RagIntake.py`

   * Loads and chunks documents
   * Creates Chunk objects
3. Run `VectorStore.py`

   * Creates embeddings
   * Builds FAISS index
   * Stores Documents
   * Runs similarity queries

---

## 🧠 Current Capabilities

* PDF loading
* Recursive chunking
* Junk filtering
* Chunk → Document conversion
* FAISS vector store
* Similarity search
* Metadata returned with results

---

## 🚧 Planned Extensions

* Retrieval score threshold gating
* Logging similarity scores
* Conversation memory
* LangGraph + MemorySaver
* Answer citations
* Persist FAISS index to disk

---

## 📖 References

* LangChain RAG Tutorial
* LangChain FAISS Integration
* LangChain Memory Concepts

---

## ⚠️ Notes

This repository prioritizes clarity over optimization.
Expect refactors as understanding improves.

---

## 🧑‍💻 Author

Joel Falconer
