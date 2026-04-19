# main.py
import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.chains import RetrievalQA
from langchain_classic.prompts import PromptTemplate

load_dotenv()

embedder = HuggingFaceEmbeddings(model_name=os.environ["HF_EMBEDDING_MODEL"])
llm = ChatAnthropic(
    model=os.environ["ANTHROPIC_MODEL"],
    temperature=0,
    api_key=os.environ["ANTHROPIC_API_KEY"],
)

# --- Build the vector store ---
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embedder)

# --- Ingest docs if store is empty ---
if vectorstore._collection.count() == 0:
    from langchain_community.document_loaders import DirectoryLoader, TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    loader = DirectoryLoader("./docs", glob="**/*.txt", loader_cls=TextLoader)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    vectorstore.add_documents(chunks)
    print(f"Ingested {len(chunks)} chunks from {len(docs)} document(s).")
else:
    print(
        f"Vector store already has {vectorstore._collection.count()} chunks, skipping ingestion."
    )

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

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
result = qa_chain.invoke({"query": "How does FHIR handle patient data?"})

print("Answer:", result["result"])
print("\nSources:")
for doc in result["source_documents"]:
    print(" -", doc.page_content)
