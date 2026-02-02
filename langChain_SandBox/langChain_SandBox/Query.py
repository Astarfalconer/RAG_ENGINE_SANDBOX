from VectorStorage import vector_store, is_within_threshold, threshold
from langchain_community.retrievers import BM25Retriever
from RagIntake import chunkDataList, docs
from QueryReWrite import rewrite_query
import nltk
nltk.download("punkt_tab")
from nltk.tokenize import word_tokenize



query = "Who can use swords in this game?"
prompt = f"Rewrite the following query to improve its clarity and specificity for improved retrieval: \n\n'{query}'"



k = 5
bm25_retriever = BM25Retriever.from_documents(
        docs,
        k=k,
        preprocess_func=word_tokenize,
        )
bm25_retriever.k = k




def get_Answer(query:str,k:int=5):
        vector = vector_store.similarity_search_with_score(query, k=k)
        filtered_vector = []
        for doc, score in vector:
         if is_within_threshold(score, threshold):
          filtered_vector.append((doc))
        return filtered_vector
def get_BM25_Answer(query:str,k:int=2):
        bm25_docs = bm25_retriever.invoke(query)
        return bm25_docs

def get_answer_for_both(query:str):
    print("Vector Store Results:")
    get_Answer(query)
    print("\nBM25 Results:")
    get_BM25_Answer(query)

def get_merged_answers(query:str):
     merged = []
     seen = set()
     BM25_docs = get_BM25_Answer(query, k=2)
     V_store_docs = get_Answer(query=query, k=2)
     for item in BM25_docs + V_store_docs:
        
      key = (item.metadata.get("chunk_id"),item.metadata.get("source",""), item.metadata.get("page",""), item.page_content)
      if key in seen:
       continue
      else:
       seen.add(key)
       merged.append(item)      
     print(f"Number of merged documents: {len(merged)}")
     print("==============================")
     print(f"Original Query: {query}")
     print("==============================")
     print("Merged Documents:")
     for doc in merged:
      page = doc.metadata.get("page", "N/A")
      print(f"Source Page: {page}")
      print(doc.page_content[:4000])  # Print first 500 characters
      print("-----")      
      print("==============================")
      print("==============================")
      print("==============================")

def get_merged_answers_reWrite(query:str):
         merged = []
         seen = set()
         rewritten_query = rewrite_query(query)
         BM25_docs = get_BM25_Answer(rewritten_query, k=2)
         V_store_docs = get_Answer(query=rewritten_query, k=2)
         for item in BM25_docs + V_store_docs:
        
          key = (item.metadata.get("chunk_id"),item.metadata.get("source",""), item.metadata.get("page",""), item.page_content)
          if key in seen:
           continue
          else:
           seen.add(key)
           merged.append(item)      
        # print(f"Number of merged documents: {len(merged)}")
         #print("==============================")
         #print(f"Original Query: {query}")
         #print("==============================")
         #print(f"Rewritten Query: {rewritten_query}")
         #print("Merged Documents:")
         for doc in merged:
          page = doc.metadata.get("page", "N/A")
          #print(f"Source Page: {page}")
          #print(doc.page_content[:4000])  # Print first 500 characters
          #print("-----")      
          #print("==============================")
          #print("==============================")
          #print("==============================")

#get_merged_answers(query)
get_merged_answers_reWrite(query)   