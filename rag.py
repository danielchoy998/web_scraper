import os 
from langchain.chat_models import init_chat_model
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import asyncio
# llm for query
llm = init_chat_model("ollama:qwen3:4b")

embeddings = OllamaEmbeddings(
    model="nomic-embed-text:latest",
)


vector_store = Chroma(
collection_name="example_collection",
embedding_function=embeddings,
persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)
  

def add_pdf_files(file_path: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_splits = text_splitter.split_documents(docs)
    # print(type(all_splits))
    # print(f"{all_splits[0].metadata}\n")
    # print(all_splits[0].page_content)
    _ = vector_store.add_documents(documents=all_splits)
    
    
def retrieve(query: str):
    retriever = vector_store.as_retriever()
    docs = retriever.invoke(query, k=2)
    serialized = "\n\n".join(
        (f"Content: {doc.page_content}")
        for doc in docs
    )
    return serialized

def main():
    # testing for RAG Process
    # print(llm.invoke("Hello, how are you?"))
    # print(embeddings.embed_query("Hello, how are you?"))
    # load_pdf_files()
    print(retrieve("What is Vision-Language Modeling?"))
if __name__ == "__main__":
    main()

    
