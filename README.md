# 🌍 AIgente-Turístico

Sistema Inteligente de Planejamento de Viagens utilizando **LangChain**, **Groq**, **Pinecone** e **Retrieval-Augmented Generation (RAG)**.


![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.x-1C3C3C?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-Qwen3.8--27B-F55036?style=for-the-badge)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20Database-0056D2?style=for-the-badge)
![RAG](https://img.shields.io/badge/RAG-Retrieval--Augmented--Generation-success?style=for-the-badge)

---
O sistema identifica automaticamente a intenção da consulta do usuário através de uma **Router Chain** e encaminha a pergunta para uma cadeia especializada.

---

## 🚀 Funcionalidades

- 📅 Geração de roteiros personalizados
- 📍 Informações turísticas utilizando RAG
- 🚇 Logística e transporte
- 🌐 Tradução de frases para viagens
- 🧠 Classificação automática de consultas
- 🔎 Busca vetorial utilizando Pinecone

---

## 🏗 Arquitetura

```text
                Usuário
                    │
                    ▼
             Router Chain
                    │
     ┌──────────────┼──────────────┐
     ▼              ▼              ▼
 Itinerary      Local Info     Logistics
     │              │              │
     └──────────────┼──────────────┘
                    ▼
            Retriever (MMR)
                    │
                    ▼
             Pinecone Vector DB
                    │
                    ▼
      Sentence Transformers
                    │
                    ▼
           Qwen 3.8-27B (Groq)
```

---

## 🛠 Tecnologias

- Python 3.10+
- LangChain 1.x
- Groq
- Pinecone
- Sentence Transformers
- LangChain HuggingFace
- Python Dotenv

---

## 📁 Estrutura do Projeto

```text
AIgente-Turistico/
│
├── knowledge_base/
│   ├── paris.txt
│   └── rio_de_janeiro.txt
│
├── chains.py
├── vector_store.py
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/AIgente-Turistico.git

cd AIgente-Turistico
```

Crie um ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente:

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## 🔑 Configuração

Crie um arquivo `.env`:

```env
GROQ_API_KEY="SUA_CHAVE"

PINECONE_API_KEY="SUA_CHAVE"

PINECONE_INDEX_NAME="aigente-turistico"
```

---

## ▶️ Execução

Execute:

```bash
python main.py
```

Na inicialização o sistema:

- Atualiza a Base de Conhecimento;
- Gera os embeddings;
- Indexa os documentos no Pinecone;
- Inicializa o modelo Qwen;
- Inicia a interface CLI.

---

## 💬 Exemplos

### Criar roteiro

```text
Monte um roteiro de 3 dias em Paris.
```

### Informações locais

```text
Quais são os restaurantes veganos do Rio de Janeiro?
```

### Logística

```text
Como ir do aeroporto Charles de Gaulle ao centro de Paris?
```

### Tradução

```text
Como dizer "Obrigado" em francês?
```

---

## 🧠 Funcionamento

1. O usuário envia uma pergunta.

2. A Router Chain identifica a intenção.

3. A consulta é enviada para a Chain especializada.

4. O Retriever busca informações no Pinecone.

5. O modelo Qwen gera a resposta utilizando RAG quando necessário.

---

## ✨ Funcionalidades Implementadas

- Router Chain
- Itinerary Chain
- Local Info Chain
- Logistics Chain
- Translation Chain
- RAG com Pinecone
- Embeddings com Sentence Transformers
- Busca vetorial MMR
- Interface CLI

---

## 📄 Licença

Projeto desenvolvido para fins acadêmicos na disciplina de **Inteligência Artificial na Prática**.
