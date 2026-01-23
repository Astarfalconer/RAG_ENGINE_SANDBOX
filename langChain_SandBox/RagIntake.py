from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

file_path = r"ExampleData\DnD_BasicRules_2018.pdf"
file_path2 = r"ExampleData\IBJJF-Rules-Version-4.pdf"
loadFile = PyPDFLoader(file_path2) 
docs = loadFile.load()
#print(docs[5].page_content[:500])

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True,
)

texts = text_splitter.split_documents(docs)

#print(f"Number of text chunks: {len(texts)}")
#print(f"First text chunk:\n{texts[15].metadata['page']}\n{texts[15].page_content}")