# main.py
import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.chains import RetrievalQA
from langchain_classic.prompts import PromptTemplate

load_dotenv()

embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
llm = ChatAnthropic(
    model="claude-sonnet-4-6", temperature=0, api_key=os.environ["ANTHROPIC_API_KEY"]
)

vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embedder)

if vectorstore._collection.count() == 0:
    print("Vector store is empty. Run `python ingest.py` first.")
    exit(1)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

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

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=True,
)

query = "What is this book about?"
result = qa_chain.invoke({"query": query})

print("Answer:", result["result"])
print("\nSources:")
for doc in result["source_documents"]:
    print(" -", doc.page_content[:200])
