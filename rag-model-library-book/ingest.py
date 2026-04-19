# ingest.py
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embedder)

if vectorstore._collection.count() > 0:
    print(
        f"Vector store already has {vectorstore._collection.count()} chunks. Delete chroma_db/ to re-ingest."
    )
else:
    txt_loader = DirectoryLoader("./data", glob="**/*.txt", loader_cls=TextLoader)
    pdf_loader = DirectoryLoader("./data", glob="**/*.pdf", loader_cls=PyPDFLoader)
    docs = txt_loader.load() + pdf_loader.load()

    if not docs:
        print("No documents found in ./data — add .txt or .pdf files and rerun.")
    else:
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.split_documents(docs)
        vectorstore.add_documents(chunks)
        print(f"Ingested {len(chunks)} chunks from {len(docs)} document(s).")
