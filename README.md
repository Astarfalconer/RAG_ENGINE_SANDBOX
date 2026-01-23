# LangChain Vector Storage & Retrieval Sandbox

This repository is a **local experimentation sandbox** for exploring **advanced vector storage and retrieval workflows using LangChain**.

The focus is on **understanding the mechanics of RAG pipelines** at a low level — document ingestion, chunking, embedding, indexing, and similarity search — without introducing agents, tools, or UI layers.

---

## Purpose

This project is designed to:

* Build intuition around **how LangChain handles vector storage**
* Experiment with **chunking strategies** and their effect on retrieval quality
* Understand **FAISS indexing** and similarity search behavior
* Inspect retrieved context **before** introducing LLM generation
* Serve as a safe “play box” for debugging and learning RAG systems

This is **not** a production system — it is intentionally minimal and inspectable.

---

## What’s Implemented

* **PDF ingestion** → page-level `Document` objects
* **Text chunking** → embedding-sized `Document` chunks with preserved metadata
* **OpenAI embeddings** → vectorization of chunks
* **FAISS (local)** → in-memory vector index
* **Similarity search** → retrieve top-K relevant chunks by query

All storage and retrieval happens **locally**.

---

## Project Structure (Conceptual)

* `RagIntake.py`
  Handles PDF loading and chunking (Parts 1–2)

* `VectorStorage.py`
  Builds the FAISS index, stores embeddings, and performs similarity search (Part 3)

---

## Scope (Intentional Limits)

* No agents
* No tool calling
* No orchestration logic
* No deployment
* No UI

The goal is to **understand retrieval quality first**, before layering on generation or agents.

---

## Why This Matters

In real-world LangChain systems, many failures attributed to “the LLM” are actually:

* poor chunking
* weak retrieval
* context loss
* noisy documents

This sandbox isolates those variables so they can be reasoned about directly.

---

## Status

* ✔ Ingestion
* ✔ Chunking
* ✔ Embedding
* ✔ FAISS indexing
* ✔ Similarity search

Next steps (optional):

* Retrieval evaluation with paraphrased queries
* Context filtering / cleanup
* RAG answer generation

---

## Notes

All documents used are for **local learning purposes only**.
No data is published or shared.

---

*Built as a focused learning environment for understanding LangChain’s vector storage layer.*
