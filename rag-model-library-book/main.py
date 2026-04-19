# main.py
import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
)
from langchain_classic.chains import RetrievalQA
from langchain_classic.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# --- Setup ---
embedder = HuggingFaceEmbeddings(
    model_name=os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
)
llm = ChatAnthropic(
    model=os.environ.get("LLM_MODEL", "claude-sonnet-4-6"),
    temperature=0,
    api_key=os.environ["ANTHROPIC_API_KEY"],
)

# --- Build the vector store ---
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embedder)

# --- Ingest docs if store is empty ---
if vectorstore._collection.count() == 0:
    txt_loader = DirectoryLoader("./data", glob="**/*.txt", loader_cls=TextLoader)
    pdf_loader = DirectoryLoader("./data", glob="**/*.pdf", loader_cls=PyPDFLoader)
    docs = txt_loader.load() + pdf_loader.load()

    if not docs:
        print("No documents found in ./data — add .txt or .pdf files and rerun.")
        exit(1)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    vectorstore.add_documents(chunks)
    print(f"Ingested {len(chunks)} chunks from {len(docs)} document(s).")
else:
    print(
        f"Vector store already has {vectorstore._collection.count()} chunks, skipping ingestion."
    )

# --- Build the retriever ---
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# --- Optional: custom prompt ---
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful assistant. Use only the context below to answer the question.
If the answer isn't in the context, say you don't know.

Context:
{context}

Question: {question}
Answer:""",
)

# --- Wire it together ---
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # "stuff" = shove all retrieved chunks into one prompt
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=True,  # so you can see what was retrieved
)

# --- Ask a question ---
query = "What is this book about?"
result = qa_chain.invoke({"query": query})

print("Answer:", result["result"])
print("\nSources:")
for doc in result["source_documents"]:
    print(" -", doc.page_content[:200])
