import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough,
)

from vector_store import obter_retriever


# -------------------------------------------------------------------
# 1. Carregar variáveis de ambiente
# -------------------------------------------------------------------

load_dotenv()


# -------------------------------------------------------------------
# 2. Inicializar o LLM via Groq
# -------------------------------------------------------------------

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="openai/gpt-oss-20b",
    temperature=0.3,
)


# -------------------------------------------------------------------
# Funções Auxiliares para o RAG (Lazy Loading do Retriever)
# -------------------------------------------------------------------

def format_docs(docs):
    """
    Formata os documentos recuperados pelo Pinecone em um único bloco de texto.
    """
    if not docs:
        return "Nenhuma informação específica encontrada na base de conhecimento."

    return "\n\n".join(
        f"--- Documento ---\n{doc.page_content}"
        for doc in docs
    )


def buscar_contexto_rag(query: str) -> str:
    """
    Instancia o retriever sob demanda e busca os documentos mais relevantes.
    """
    retriever = obter_retriever()
    docs = retriever.invoke(query)

    return format_docs(docs)


# -------------------------------------------------------------------
# 1. ITINERARY CHAIN (Roteiro de Viagem - Utiliza RAG)
# -------------------------------------------------------------------

itinerary_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Você é um especialista em criação de roteiros de viagem personalizados.

Utilize as informações do contexto abaixo para criar um itinerário detalhado dia a dia.

Se o contexto não contiver todas as informações necessárias,
crie sugestões coerentes baseadas no seu conhecimento,
mantendo o foco no perfil solicitado.

Contexto Relevante da Base de Conhecimento:

{context}
""",
        ),
        ("human", "{input}"),
    ]
)

itinerary_chain = (
    {
        "context": RunnableLambda(buscar_contexto_rag),
        "input": RunnablePassthrough(),
    }
    | itinerary_prompt
    | llm
    | StrOutputParser()
)


# -------------------------------------------------------------------
# 2. LOGISTICS CHAIN (Logística e Transporte)
# -------------------------------------------------------------------

logistics_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Você é um assistente especialista em logística de viagens e transportes.

Forneça orientações práticas e objetivas sobre como se locomover,
transporte público/privado, deslocamentos entre aeroportos,
estações e hotéis, além de dicas de segurança.
""",
        ),
        ("human", "{input}"),
    ]
)

logistics_chain = (
    logistics_prompt
    | llm
    | StrOutputParser()
)


# -------------------------------------------------------------------
# 3. LOCAL INFO CHAIN (Informações Locais - Utiliza RAG)
# -------------------------------------------------------------------

local_info_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Você é um guia turístico local altamente informado.

Responda às perguntas sobre pontos turísticos,
restaurantes, horários de funcionamento,
ingressos e dicas locais.

Baseie-se rigorosamente no contexto fornecido.

Se a informação não estiver disponível no contexto,
informe educadamente que não possui esse detalhe específico
na base.

Contexto Relevante da Base de Conhecimento:

{context}
""",
        ),
        ("human", "{input}"),
    ]
)

local_info_chain = (
    {
        "context": RunnableLambda(buscar_contexto_rag),
        "input": RunnablePassthrough(),
    }
    | local_info_prompt
    | llm
    | StrOutputParser()
)


# -------------------------------------------------------------------
# 4. TRANSLATION CHAIN (Guia de Tradução - Bônus)
# -------------------------------------------------------------------

translation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Você é um tradutor e guia linguístico para viajantes.

Forneça a tradução solicitada,
acompanhada da pronúncia aproximada em português
e exemplos de frases úteis para situações reais de viagem
(ex.: pedir a conta, cumprimentar, pedir ajuda).
""",
        ),
        ("human", "{input}"),
    ]
)

translation_chain = (
    translation_prompt
    | llm
    | StrOutputParser()
)


# -------------------------------------------------------------------
# 5. ROUTER CHAIN (Classificador de Intenção)
# -------------------------------------------------------------------

router_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Você é um classificador de intenção de consultas turísticas.

Analise a pergunta do usuário e responda APENAS com uma das
seguintes palavras-chave (sem texto adicional,
pontuação ou explicações):

- roteiro-viagem : Se a pergunta pedir um itinerário,
  plano de dias ou sugestão de roteiro.

- logistica-transporte : Se a pergunta for sobre transporte,
  trajetos, metrô, voos ou como ir de um lugar a outro.

- info-local : Se a pergunta for sobre pontos turísticos,
  atrações, restaurantes, horários ou ingressos.

- traducao-idiomas : Se a pergunta for sobre tradução
  de frases, expressões úteis ou idioma local.

- geral : Se a pergunta não se encaixar claramente
  em nenhuma das categorias anteriores.
""",
        ),
        ("human", "{input}"),
    ]
)

router_chain = (
    router_prompt
    | llm
    | StrOutputParser()
)


# -------------------------------------------------------------------
# Função Principal de Orquestração do Roteador
# -------------------------------------------------------------------

def processar_consulta(consulta_usuario: str):
    """
    Classifica a consulta do usuário e a direciona
    para a cadeia especializada correspondente.
    """

    # 1. Classificar intenção via Router Chain
    categoria_raw = router_chain.invoke({"input": consulta_usuario})
    categoria = categoria_raw.strip().lower()

    print(f"🎯 [Router Chain] Classificação obtida: '{categoria}'")

    # 2. Direcionar para a cadeia responsável
    if "roteiro-viagem" in categoria:
        resposta = itinerary_chain.invoke(consulta_usuario)
        cadeia_usada = "Itinerary Chain (roteiro-viagem)"

    elif "logistica-transporte" in categoria:
        resposta = logistics_chain.invoke({"input": consulta_usuario})
        cadeia_usada = "Logistics Chain (logistica-transporte)"

    elif "info-local" in categoria:
        resposta = local_info_chain.invoke(consulta_usuario)
        cadeia_usada = "Local Info Chain (info-local)"

    elif "traducao-idiomas" in categoria:
        resposta = translation_chain.invoke({"input": consulta_usuario})
        cadeia_usada = "Translation Chain (traducao-idiomas)"

    else:
        # Fallback para consultas gerais
        resposta = local_info_chain.invoke(consulta_usuario)
        cadeia_usada = "Local Info Chain (Modo Geral)"

    return categoria, cadeia_usada, resposta