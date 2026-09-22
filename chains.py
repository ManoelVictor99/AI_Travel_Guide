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


# ==========================================================
# Carregar variáveis de ambiente
# ==========================================================

load_dotenv()


# ==========================================================
# Inicialização do LLM
# ==========================================================

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="qwen/qwen3.8-27b",
    temperature=0.2,
    max_tokens=1024,
)


# ==========================================================
# Funções auxiliares do RAG
# ==========================================================

def format_docs(docs):
    """
    Concatena os documentos recuperados pelo Pinecone.
    """

    if not docs:
        return (
            "Nenhuma informação relevante foi encontrada "
            "na base de conhecimento."
        )

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


def buscar_contexto_rag(query: str) -> str:
    """
    Recupera os documentos mais relevantes da base vetorial.
    """

    retriever = obter_retriever()

    docs = retriever.invoke(query)

    return format_docs(docs)


# ==========================================================
# 1. ITINERARY CHAIN
# ==========================================================

itinerary_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Você é um especialista em planejamento de viagens.

Utilize PRIMEIRAMENTE o contexto fornecido.

Caso alguma informação não esteja presente,
complemente utilizando seu conhecimento.

Responda sempre em texto simples.

Não utilize Markdown.

Não utilize tabelas.

Organize a resposta por dias.

Exemplo:

Dia 1
- ...

Dia 2
- ...

Dia 3
- ...

Contexto:

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

# ==========================================================
# 2. LOGISTICS CHAIN
# ==========================================================

logistics_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Você é um especialista em logística de viagens.

Utilize PRIMEIRAMENTE o contexto recuperado da base de conhecimento.

Caso alguma informação não esteja presente,
complemente utilizando seu conhecimento.

Responda sempre em texto simples.

Não utilize Markdown.

Não utilize tabelas.

Organize a resposta em tópicos.

Sempre que possível informe:

- Meio de transporte
- Tempo estimado
- Custos aproximados
- Dicas úteis ao turista

Contexto:

{context}
""",
        ),
        ("human", "{input}"),
    ]
)

logistics_chain = (
    {
        "context": RunnableLambda(buscar_contexto_rag),
        "input": RunnablePassthrough(),
    }
    | logistics_prompt
    | llm
    | StrOutputParser()
)


# ==========================================================
# 3. LOCAL INFO CHAIN
# ==========================================================

local_info_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Você é um guia turístico especializado.

Responda utilizando prioritariamente o contexto fornecido.

Caso a informação não exista no contexto,
informe isso educadamente e complemente apenas
com conhecimento geral quando apropriado.

Responda sempre em texto simples.

Não utilize Markdown.

Não utilize tabelas.

Não utilize negrito.

Organize a resposta em tópicos.

Quando listar restaurantes, atrações ou locais,
utilize o seguinte formato:

• Nome
  - Localização
  - Breve descrição

Contexto:

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


# ==========================================================
# 4. TRANSLATION CHAIN
# ==========================================================

translation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Você é um tradutor para turistas.

Forneça:

- Tradução
- Pronúncia aproximada em português
- Um exemplo de utilização

Responda em texto simples.

Não utilize Markdown.

Não utilize tabelas.
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

# ==========================================================
# 5. ROUTER CHAIN
# ==========================================================

router_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Você é um classificador de intenção para um assistente de viagens.

Analise a pergunta do usuário e responda APENAS com uma das
seguintes categorias.

Não explique.
Não escreva frases.
Não utilize pontuação.

Categorias disponíveis:

roteiro-viagem
logistica-transporte
info-local
traducao-idiomas
geral
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


# ==========================================================
# Função Principal
# ==========================================================

def processar_consulta(consulta_usuario: str):
    """
    Classifica a intenção do usuário e direciona
    automaticamente para a chain especializada.
    """

    categoria = (
        router_chain.invoke(
            {"input": consulta_usuario}
        )
        .strip()
        .lower()
    )

    print(f"🎯 [Router Chain] Classificação obtida: '{categoria}'")

    if categoria == "roteiro-viagem":

        resposta = itinerary_chain.invoke(consulta_usuario)

        cadeia_usada = "Itinerary Chain"

    elif categoria == "logistica-transporte":

        resposta = logistics_chain.invoke(consulta_usuario)

        cadeia_usada = "Logistics Chain"

    elif categoria == "info-local":

        resposta = local_info_chain.invoke(consulta_usuario)

        cadeia_usada = "Local Info Chain"

    elif categoria == "traducao-idiomas":

        resposta = translation_chain.invoke(
            {"input": consulta_usuario}
        )

        cadeia_usada = "Translation Chain"

    else:

        # Caso o Router não identifique corretamente,
        # utiliza a cadeia mais abrangente.

        resposta = local_info_chain.invoke(consulta_usuario)

        cadeia_usada = "Local Info Chain"

    return (
        categoria,
        cadeia_usada,
        resposta,
    )
