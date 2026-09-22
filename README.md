🌍 AIgente-Turístico: Sistema Inteligente de Guia de Viagens com RAG

Descrição

O AIgente-Turístico é um assistente inteligente para planejamento de
viagens desenvolvido em Python utilizando LangChain, Groq, Pinecone e
RAG (Retrieval-Augmented Generation).

O sistema classifica automaticamente a intenção da consulta do usuário
por meio de uma Router Chain e direciona a pergunta para uma cadeia
especializada:

-   Itinerary Chain – criação de roteiros personalizados.
-   Local Info Chain – informações sobre atrações, restaurantes e pontos
    turísticos utilizando RAG.
-   Logistics Chain – logística e transporte utilizando RAG.
-   Translation Chain – tradução de frases úteis para viagens.

A base de conhecimento é composta por arquivos .txt armazenados na pasta
knowledge_base, indexados no Pinecone utilizando embeddings do modelo
sentence-transformers/all-MiniLM-L6-v2.

------------------------------------------------------------------------

Tecnologias Utilizadas

-   Python 3.10+
-   LangChain 1.x
-   LangChain Community
-   LangChain HuggingFace
-   LangChain Pinecone
-   LangChain Groq
-   Pinecone
-   Groq API
-   Qwen 3.8 27B
-   Sentence Transformers
-   Python Dotenv

------------------------------------------------------------------------

Arquitetura

Usuário │ ▼ Router Chain │ ├──────────────┐ │ │ ▼ ▼ Itinerary Local Info
│ │ ├──────┬───────┘ │ │ ▼ ▼ Logistics Translation │ ▼ Retriever (MMR) │
▼ Pinecone │ ▼ Embeddings │ ▼ Qwen (Groq)

------------------------------------------------------------------------

Estrutura do Projeto

AIgente-Turistico/ │ ├── knowledge_base/ │ ├── paris.txt │ └──
rio_de_janeiro.txt │ ├── chains.py ├── vector_store.py ├── main.py ├──
requirements.txt ├── .env.example ├── README.md

------------------------------------------------------------------------

Instalação

1.  Clone o repositório

git clone https://github.com/SEU_USUARIO/AIgente-turistico.git

2.  Crie um ambiente virtual

python -m venv venv

3.  Ative o ambiente

Windows: venv

Linux/macOS: source venv/bin/activate

4.  Instale as dependências

pip install -r requirements.txt

5.  Configure o arquivo .env

GROQ_API_KEY=“SUA_CHAVE” PINECONE_API_KEY=“SUA_CHAVE”
PINECONE_INDEX_NAME=“aigente-turistico”

------------------------------------------------------------------------

Execução

python main.py

Na inicialização o sistema:

-   Indexa automaticamente a base de conhecimento.
-   Atualiza o índice do Pinecone.
-   Carrega o modelo Qwen.
-   Inicia a interface CLI.

------------------------------------------------------------------------

Exemplos

Monte um roteiro de 3 dias em Paris.

Quais são os restaurantes veganos do Rio de Janeiro?

Como ir do aeroporto Charles de Gaulle ao centro de Paris?

Como dizer “Onde fica o banheiro?” em francês?

------------------------------------------------------------------------

Melhorias Implementadas

-   Router Chain para classificação automática.
-   Arquitetura RAG utilizando Pinecone.
-   Busca vetorial utilizando MMR.
-   Reindexação automática evitando documentos duplicados.
-   Cadeias especializadas para diferentes tipos de consultas.
-   Embeddings utilizando all-MiniLM-L6-v2.
-   Integração com Groq utilizando o modelo qwen/qwen3.8-27b.
-   Interface de linha de comando.

------------------------------------------------------------------------

Próximas Melhorias

-   Inclusão de novas cidades.
-   Histórico de conversas.
-   Interface Web.
-   Geração de mapas.
-   Reserva de hotéis e voos.
-   Memória conversacional.

------------------------------------------------------------------------

Licença

Projeto desenvolvido para fins acadêmicos na disciplina de Inteligência
Artificial na Prática.
