
from langchain_openai import OpenAIEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from uuid import uuid4
from langchain_core.documents import Document
from yarl import Query    
from RagIntake import chunkDataList
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
example = len(embeddings.embed_query("Hello world"))
index = faiss.IndexFlatL2(example)
vector_store = FAISS(
    index=index,
    embedding_function=embeddings,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

uuids = [str(uuid4()) for _ in range(len(chunkDataList))]

def is_within_threshold(score: float, threshold: float) -> bool:
    return score <= threshold

Documents = [
    Document(
        page_content=chunk.content,
        metadata={
            "chunk_id": chunk.chunk_id,
            "page": chunk.page,
            "source": chunk.source
        }
    )
    for chunk in chunkDataList
]
threshold = 0.96
vector_store.add_documents(documents=Documents, ids=uuids)
print(f"Number of vectors in store: {vector_store.index.ntotal}")


