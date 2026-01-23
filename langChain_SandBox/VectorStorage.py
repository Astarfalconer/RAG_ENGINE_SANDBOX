from langchain_openai import OpenAIEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from uuid import uuid4
from langchain_core.documents import Document    
from RagIntake import texts
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

example = len(embeddings.embed_query("Hello world"))
index = faiss.IndexFlatL2(example)
vector_store = FAISS(
    index=index,
    embedding_function=embeddings,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

uuids = [str(uuid4()) for _ in range(len(texts))]
vector_store.add_documents(documents=texts, ids=uuids)
print(f"Number of vectors in store: {vector_store.index.ntotal}")
vector = vector_store.similarity_search("what are submissions?", k=2)
print("Top 2 similar documents:")
for doc in vector:
    print(doc.page_content) 