
from langchain_openai import OpenAIEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from uuid import uuid4
from langchain_core.documents import Document    
from RagIntake import chunkDataList
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
filtered_vector = []
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
    print("FUNCTION CALLED!!!2")
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
threshold = 0.956
vector_store.add_documents(documents=Documents, ids=uuids)
print(f"Number of vectors in store: {vector_store.index.ntotal}")
vector = vector_store.similarity_search_with_score("how does health work?", k=5)
for doc, score in vector:
    if is_within_threshold(score, threshold):
        filtered_vector.append((doc, score))
    


print(f"Number of documents within threshold: {len(filtered_vector)}")

##print("Top 2 similar documents:")
for doc, score in filtered_vector:
    print(doc.page_content)
    print(f"Score: {score}")
    print("-----")
    print(doc.metadata) 