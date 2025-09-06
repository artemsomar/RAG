# Retrieval-Augmented Generation system

This project is a **Retrieval-Augmented Generation (RAG)** system developed with **FastAPI** as the backend framework and **Cohere** for embedding and language modeling. The system combines efficient document retrieval with semantic understanding to generate more accurate, context-aware answers.

The architecture leverages **BM25** for keyword-based search and **semantic similarity search** powered by embeddings, enabling a **hybrid retrieval strategy**. Retrieved document chunks are processed, ranked, and then passed to a generative model to provide meaningful responses enriched with source context.

The system is designed with modularity in mind: document chunking, embedding, retrieval, and generation are implemented as independent components, allowing flexible customization and future extensions. Data is stored and managed using **PostgreSQL**, with **SQLAlchemy** for ORM support. The service is built on **asynchronous Python**, making it scalable and efficient for larger workloads.

Please note that the system is **still under active development**.

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development

### Installing

A step by step series of examples that tell you how to get a development
environment running

Clone the repository

    git clone https://github.com/artemsomar/RAG.git
    cd RAG
    
Install Poetry

    pip install poetry

Install dependencies with Poetry

    poetry install
    
Activate the virtual environment

    poetry shell
    
Configure environment variables (create a .env file in the project root and add your settings):

    DB__USER=your_db_user
    DB__PASSWORD=your_db_password

    EMBEDDING__TOKEN=your_cohere_token

    TOKENIZING__TOKEN=your_cohere_token
    
Generate migrations

    alembic revision --autogenerate -m "init"
    alembic upgrade head
    
Start the application

    python -m src.app

The API will be available at:
http://127.0.0.1:8000

You can interact with the system via HTTP requests. First, add documents to the system by sending a **POST** request to the
*/documents/* endpoint. Once your documents are added, you can query for relevant sections using the */rag/* endpoint, which
returns the chunks of documents that best match your query. Finally, to get a comprehensive answer based on your documents,
send a request to the */llm_rag/* endpoint; the system will generate a response that references the previously added documents. 
