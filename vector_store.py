import glob
import os

from dotenv import load_dotenv

from pinecone import Pinecone, ServerlessSpec

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore


# ==========================================================
# Carregar variáveis de ambiente
# ==========================================================

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME",
    "aigente-turistico"
)


# ==========================================================
# Modelo de Embeddings
# ==========================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ==========================================================
# Indexação da Base
# ==========================================================

def indexar_base_de_conhecimento():

    print("🚀 Verificando base de conhecimento...")

    if not PINECONE_API_KEY:
        raise ValueError(
            "PINECONE_API_KEY não encontrada."
        )

    pc = Pinecone(
        api_key=PINECONE_API_KEY
    )

    embedding_dim = 384

    indices = [
        idx.name
        for idx in pc.list_indexes()
    ]

    if INDEX_NAME not in indices:

        print(f"Criando índice '{INDEX_NAME}'...")

        pc.create_index(
            name=INDEX_NAME,
            dimension=embedding_dim,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            ),
        )

    index = pc.Index(INDEX_NAME)

    print("Atualizando índice...")

    index.delete(delete_all=True)

    arquivos = glob.glob(
        "knowledge_base/*.txt"
    )

    if not arquivos:
        raise FileNotFoundError(
            "Nenhum arquivo encontrado em knowledge_base/"
        )

    documentos = []

    for arquivo in arquivos:

        loader = TextLoader(
            arquivo,
            encoding="utf-8"
        )

        documentos.extend(
            loader.load()
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = splitter.split_documents(
        documentos
    )

    PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=INDEX_NAME,
    )

    print(
        f"✅ Base indexada com sucesso "
        f"({len(chunks)} chunks)."
    )


# ==========================================================
# Retriever
# ==========================================================

def obter_retriever():

    vectorstore = PineconeVectorStore(
        index_name=INDEX_NAME,
        embedding=embeddings,
    )

    return vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 4,
            "fetch_k": 10,
        },
    )
