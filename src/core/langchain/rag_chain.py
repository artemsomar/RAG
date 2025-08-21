import os
from src.dataset_loader import DatasetLoader
from dotenv import load_dotenv
from langchain_cohere import ChatCohere, CohereEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

load_dotenv()

def rag_chain(query):
    df_loader = DatasetLoader()
    dataset = df_loader.load()
    texts = [f"{item['title']}\t{item['abstract']}" for item in dataset]
    metadata = [{"citation": f"{item['title']}"} for item in dataset]

    embeddings = CohereEmbeddings(cohere_api_key=os.getenv("CO_TOKEN"), model="embed-english-light-v3.0")
    vectorstore = Chroma.from_texts(texts, embedding=embeddings, metadatas=metadata)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    llm = ChatCohere(cohere_api_key=os.getenv("CO_TOKEN"))

    prompt = ChatPromptTemplate.from_template("""
    Use the following context to answer the question.
    If you don't know the answer, say honestly "I don't know."
    
    Context:
    {context}
    
    Quastion:
    {input}
    """)

    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    result = retrieval_chain.invoke({"input": query})
    answer = result["answer"]
    for doc in result["context"]:
        citation = doc.metadata.get("citation", "")
        answer += f"\n[{citation}]"

    return answer

# print(rag_chain(query = "How neural networks work?"))