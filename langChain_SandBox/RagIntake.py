from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy import text
from ChunkClass import ChunkClass, CreateChunk
file_path = r"ExampleData\DnD_BasicRules_2018.pdf"
file_path2 = r"ExampleData\IBJJF-Rules-Version-4.pdf"
loadFile = PyPDFLoader(file_path) 
docs = loadFile.load()
#print(docs[5].page_content[:500])

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True,
)

texts = text_splitter.split_documents(docs)
junk_markers = [
    "photos by",
    "design and illustration",
    "international brazilian jiu-jitsu federation",
    "version",
    ]

def filter_Junk(texts, junk_markers):
    filtered_texts = []
    for text in texts:
        if not any(marker.lower() in text.page_content.lower() for marker in junk_markers):
            filtered_texts.append(text)
    return filtered_texts

filtered_texts = filter_Junk(texts, junk_markers)

chunkDataList = []
for text in filtered_texts:
    chunkData = CreateChunk(
        chunk_id=f"{file_path}_p{text.metadata['page']}_{text.metadata['start_index']}",
        content=text.page_content,
        page=text.metadata['page'],
        source=file_path
    )
    chunkDataList.append(chunkData)

#print(f"Number of text chunks: {len(texts)}")
#print(f"First text chunk:\n{texts[15].metadata['page']}\n{texts[15].page_content}")