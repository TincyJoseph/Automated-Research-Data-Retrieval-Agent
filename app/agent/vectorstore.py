import os
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

DATA_PATH = "app/data/data.md"
VECTORSTORE_PATH = "app/data/faiss_index"

def get_vectorstore():
    """
    Load the vectorstore if it exists, else create it from data.md and save.
    Returns: FAISS vectorstore
    """
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 1️⃣ If vectorstore exists, load it
    if os.path.exists(VECTORSTORE_PATH):
        print(f"Loading existing vectorstore from {VECTORSTORE_PATH}...")
        vectorstore = FAISS.load_local(VECTORSTORE_PATH, embeddings, allow_dangerous_deserialization=True)
        return vectorstore

    # Else, create vectorstore
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"{DATA_PATH} not found!")

    print("Creating vectorstore from data.md...")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    doc = Document(page_content=text, metadata={"source": "data.md"})
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents([doc])

    vectorstore = FAISS.from_documents(docs, embeddings)

    # Save for future use
    vectorstore.save_local(VECTORSTORE_PATH)
    print(f"Vectorstore created and saved at {VECTORSTORE_PATH}")
    return vectorstore

