# 🌍 AIgente-Turístico: Sistema Inteligente de Guia de Viagens com RAG & Router Chains

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Llama3-F50057?style=for-the-badge&logo=groq&logoColor=white)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector_DB-000000?style=for-the-badge&logo=pinecone&logoColor=white)

O **AIgente-Turístico** é um sistema inteligente de assistência ao viajante desenvolvido para classificar automaticamente as intenções das consultas dos usuários e direcioná-las a **Cadeias Especializadas (Chains)** de processamento. A solução combina a orquestração do **LangChain**, a velocidade do motor de inferência **Groq (Llama 3)** e a técnica de **RAG (Retrieval-Augmented Generation)** utilizando o banco vetorial **Pinecone**.

---

## 🎯 1. Objetivo do Projeto

 O sistema tem como propósito demonstrar uma arquitetura modular e escalável para assistentes virtuais sem a necessidade de agentes autônomos ilimitados. Ele oferece:
- **Roteiros Personalizados**: Geração de itinerários detalhados dia a dia com base na base de conhecimento.
- **Roteamento Inteligente**: Classificação de intenções por uma *Router Chain* que direciona cada dúvida para o módulo correto.
- **Respostas Precisas via RAG**: Consulta a dados atualizados e específicos de cidades turísticas (como Rio de Janeiro e Paris) indexados em vetores.
- **Alta Velocidade de Resposta**: Inferência em tempo real fornecida pela LPU da Groq.

---

## 🛠️ 2. Arquitetura e Tecnologias

```text
                               ┌──────────────────────────┐
                               │   Consulta do Turista    │
                               └─────────────┬────────────┘
                                             │
                                             ▼
                                 ┌──────────────────────┐
                                 │     Router Chain     │
                                 │ (Classifica Intenção)│
                                 └───────────┬──────────┘
                                             │
      ┌──────────────────────┬───────────────┴───────────────┬──────────────────────┐
      │                      │                               │                      │
      ▼                      ▼                               ▼                      ▼
┌─────────────┐    ┌──────────────────┐            ┌──────────────────┐   ┌───────────────────┐
│ Itinerary   │    │ Local Info Chain │            │ Logistics Chain  │   │ Translation Chain │
│    Chain    │    │   (Info Local)   │            │   (Logística)    │   │    (Tradução)     │
└──────┬──────┘    └─────────┬────────┘            └──────────────────┘   └───────────────────┘
       │                     │
       └──────────┬──────────┘
                  │ (Busca RAG)
                  ▼
         ┌────────────────┐
         │ Pinecone DB    │
         │ (SentenceTrans)│
         └────────────────┘
```

### Principais Bibliotecas e Serviços
- **[LangChain](https://python.langchain.com/)**: Framework para orquestração de prompts, LCEL e fluxos de RAG.
- **[Groq](https://groq.com/)**: Motor de inferência de altíssimo desempenho para o modelo **Llama 3** (`llama3-8b-8192`).
- **[Pinecone](https://www.pinecone.io/)**: Banco de dados vetorial em nuvem para armazenamento dos *embeddings*.
- **[SentenceTransformers](https://www.sbert.net/)**: Modelo `sentence-transformers/all-MiniLM-L6-v2` para geração dos vetores de 384 dimensões.

---

## 📁 3. Estrutura do Repositório

```text
AIgente-turistico/
│
├── knowledge_base/               # Arquivos de dados de texto para o RAG
│   ├── paris.txt                 # Guia de atrações, restaurantes e transporte em Paris
│   └── rio_de_janeiro.txt        # Guia de atrações, restaurantes e transporte no Rio
│
├── .env.example                  # Modelo para configuração das chaves de API
├── .gitignore                    # Arquivos e pastas ignorados pelo Git
├── requirements.txt              # Lista de dependências Python
├── vector_store.py               # Script de geração de embeddings e indexação no Pinecone
├── chains.py                     # Definição do Router Chain e das Cadeias Especializadas
├── main.py                       # Interface de linha de comando (CLI) interativa
└── README.md                     # Documentação oficial do projeto
```

---

## ⚙️ 4. Configuração e Instalação

### Pré-requisitos
- **Python 3.9+** instalado.
- Chave de API gratuita da **[Groq](https://console.groq.com/)**.
- Chave de API gratuita do **[Pinecone](https://app.pinecone.io/)**.

### Passo a Passo

1. **Clonar o Repositório**:
   ```bash
   git clone https://github.com/SEU_USUARIO/AIgente-turistico.git
   cd AIgente-turistico
   ```

2. **Criar e Ativar o Ambiente Virtual**:
   - *Windows:*
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - *Linux/macOS:*
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instalar Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar Variáveis de Ambiente**:
   Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:
   ```env
   GROQ_API_KEY="sua_chave_groq_aqui"
   PINECONE_API_KEY="sua_chave_pinecone_aqui"
   PINECONE_INDEX_NAME="aigente-turistico"
   ```

---

## 🚀 5. Como Executar

### 1️⃣ Indexar a Base de Conhecimento (Executar 1x)
Processe os arquivos da pasta `knowledge_base/`, gere os vetores e crie o índice no Pinecone:
```bash
python vector_store.py
```

### 2️⃣ Iniciar o Assistente
Inicie a interface CLI do AIgente-Turístico:
```bash
python main.py
```

---

## 🧪 6. Exemplos de Consultas e Testes

Ao executar o `main.py`, você pode testar diferentes tipos de perguntas para verificar o roteamento automático:

| Tipo de Consulta | Exemplo de Pergunta | Módulo Ativado |
| :--- | :--- | :--- |
| **Roteiro de Viagem** | *"Monte um roteiro cultural de 3 dias em Paris."* | `Itinerary Chain` |
| **Informações Locais (RAG)** | *"Quais são os restaurantes veganos no Rio de Janeiro?"* | `Local Info Chain` |
| **Logística & Transporte** | *"Como ir do aeroporto Charles de Gaulle ao centro de Paris?"* | `Logistics Chain` |
| **Guia de Tradução** | *"Como pedir a conta educadamente em francês?"* | `Translation Chain` |

---

## 🤝 7. Licença e Créditos

Projeto desenvolvido como atividade acadêmica para a disciplina de **Inteligência Artificial na Prática**.
