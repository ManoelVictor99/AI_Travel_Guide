import os
import glob

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore


# 1. Carregar variáveis do .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "aigente-turistico")


def indexar_base_de_conhecimento():
    """
    Lê os arquivos de texto, gera embeddings e indexa no Pinecone.
    """
    print("🚀 Iniciando o processo de indexação no Pinecone...")

    if not PINECONE_API_KEY:
        raise ValueError("❌ PINECONE_API_KEY não configurada no arquivo .env")

    # 2. Inicializar cliente Pinecone (Nova API v3+)
    pc = Pinecone(api_key=PINECONE_API_KEY)

    # 3. Inicializar Modelo de Embeddings (384 dimensões)
    print("📦 Carregando modelo de embeddings (SentenceTransformers)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    embedding_dim = 384

    # 4. Verificar ou Criar o Índice no Pinecone
    indices_existentes = [idx.name for idx in pc.list_indexes()]

    if INDEX_NAME not in indices_existentes:
        print(f"🛠️ Criando novo índice no Pinecone: '{INDEX_NAME}'...")

        pc.create_index(
            name=INDEX_NAME,
            dimension=embedding_dim,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

        print("✅ Índice criado com sucesso!")

    else:
        print(f"ℹ️ O índice '{INDEX_NAME}' já existe no Pinecone.")

    # 5. Carregar Documentos da pasta knowledge_base/
    arquivos = glob.glob("knowledge_base/*.txt")

    if not arquivos:
        raise FileNotFoundError(
            "❌ Nenhum arquivo .txt encontrado na pasta 'knowledge_base/'."
        )

    documentos = []

    for arq in arquivos:
        print(f"📄 Lendo arquivo: {arq}")
        loader = TextLoader(arq, encoding="utf-8")
        documentos.extend(loader.load())

    # 6. Dividir Documentos em Chunks (Divisão com overlap)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documentos)

    print(f"🧩 Total de {len(chunks)} chunks gerados a partir dos documentos.")

    # 7. Salvar Chunks e Embeddings no Pinecone
    print("📤 Enviando vetores para o Pinecone...")

    vectorstore = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=INDEX_NAME
    )

    print("🎉 Base de conhecimento indexada com sucesso no Pinecone!")

    return vectorstore


def obter_retriever():
    """
    Retorna o retriever do Pinecone para ser usado nas cadeias RAG.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = PineconeVectorStore(
        index_name=INDEX_NAME,
        embedding=embeddings
    )

    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )


if __name__ == "__main__":
    indexar_base_de_conhecimento()