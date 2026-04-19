# main.py
import os
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# --- Setup (same as before) ---
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index("my-demo-index")

embedder = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"])
llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=os.environ["OPENAI_API_KEY"])

# --- Build the retriever ---
vectorstore = PineconeVectorStore(index=index, embedding=embedder)
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
