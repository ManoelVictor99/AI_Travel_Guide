# 🌍 AIgente-Turístico

### Sistema Inteligente de Planejamento de Viagens utilizando LangChain, RAG, Pinecone e Groq

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.x-1C3C3C?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-Qwen3.8--27B-F55036?style=for-the-badge)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20Database-0056D2?style=for-the-badge)
![RAG](https://img.shields.io/badge/RAG-Retrieval--Augmented--Generation-success?style=for-the-badge)

---

# 📖 Sobre o Projeto

O **AIgente-Turístico** é um sistema inteligente de assistência ao viajante desenvolvido em **Python** utilizando **LangChain**, **Groq** e **Pinecone**.

O projeto implementa uma arquitetura baseada em **Router Chains** e **Retrieval-Augmented Generation (RAG)** para responder perguntas sobre destinos turísticos de maneira rápida, organizada e contextualizada.

Em vez de utilizar um único modelo para responder qualquer pergunta, o sistema primeiro identifica a intenção do usuário e direciona automaticamente a solicitação para uma cadeia especializada.

Atualmente o sistema possui quatro módulos especializados:

- 🗺️ Criação de roteiros personalizados de viagem;
- 📍 Informações sobre atrações turísticas;
- 🚇 Logística e transporte;
- 🌐 Tradução de frases úteis para turistas.

As informações específicas de cada cidade são armazenadas em uma **Base de Conhecimento** composta por arquivos `.txt`, convertidos em embeddings e indexados no **Pinecone**, permitindo consultas utilizando **RAG**.

---

# 🎯 Objetivos

Este projeto foi desenvolvido com os seguintes objetivos:

- Demonstrar uma arquitetura moderna baseada em **LangChain**.
- Implementar um sistema de **RAG** utilizando banco vetorial.
- Utilizar **Router Chains** para classificação automática das consultas.
- Construir um assistente turístico modular e escalável.
- Explorar a utilização de **LLMs hospedados na Groq**.
- Demonstrar a integração entre modelos de linguagem e bancos vetoriais.

---

# 🏗 Arquitetura do Sistema

```text
                         Usuário
                            │
                            ▼
                  Router Chain (LLM)
                            │
      ┌─────────────────────┼─────────────────────┐
      │                     │                     │
      ▼                     ▼                     ▼
Itinerary Chain      Local Info Chain     Logistics Chain
      │                     │                     │
      └───────────────┬─────┴─────────────────────┘
                      │
                      ▼
               Retriever (MMR)
                      │
                      ▼
             Pinecone Vector Database
                      │
                      ▼
        Sentence Transformers Embeddings
                      │
                      ▼
          Modelo Qwen 3.8-27B (Groq)
                      │
                      ▼
               Resposta ao Usuário
```

---

# 🔄 Fluxo de Funcionamento

O fluxo completo da aplicação ocorre da seguinte forma:

1. O usuário realiza uma pergunta na interface de linha de comando.
2. A **Router Chain** identifica automaticamente a intenção da consulta.
3. A consulta é direcionada para a cadeia especializada correspondente.
4. Caso necessário, a cadeia consulta a Base de Conhecimento utilizando **RAG**.
5. O Retriever recupera os documentos mais relevantes no Pinecone utilizando busca **MMR (Maximal Marginal Relevance)**.
6. O contexto recuperado é enviado ao modelo de linguagem.
7. O modelo gera uma resposta personalizada ao usuário.

---

# 🛠 Tecnologias Utilizadas

## Linguagem

- Python 3.10+

## Frameworks

- LangChain
- LangChain Community
- LangChain HuggingFace
- LangChain Pinecone
- LangChain Groq

## Banco Vetorial

- Pinecone

## Modelo de Linguagem

- Qwen 3.8 27B
- Groq API

## Modelo de Embeddings

- sentence-transformers/all-MiniLM-L6-v2

## Bibliotecas

- Sentence Transformers
- Python Dotenv
- NumPy
- PyPDF

---

# ✨ Principais Funcionalidades

✅ Geração automática de roteiros de viagem

✅ Informações turísticas utilizando RAG

✅ Consulta à Base de Conhecimento através do Pinecone

✅ Tradução de frases para viagens

✅ Informações de logística e transporte

✅ Classificação automática utilizando Router Chain

✅ Arquitetura modular baseada em Chains

✅ Busca vetorial utilizando MMR

✅ Interface de linha de comando (CLI)

---
# 📁 Estrutura do Projeto

```text
AIgente-Turistico/
│
├── knowledge_base/
│   ├── paris.txt
│   └── rio_de_janeiro.txt
│
├── .env.example
├── .gitignore
├── requirements.txt
│
├── vector_store.py
├── chains.py
├── main.py
│
└── README.md
```

---

# 📂 Organização dos Arquivos

### 📁 knowledge_base/

Contém a Base de Conhecimento utilizada pelo sistema.

Cada arquivo representa um destino turístico e possui informações estruturadas sobre:

- Atrações turísticas;
- Gastronomia;
- Transporte e logística.

Esses arquivos são convertidos em embeddings durante a indexação.

---

### 📄 vector_store.py

Responsável por toda a camada de RAG.

Suas principais funções são:

- Carregar os arquivos `.txt`;
- Dividir o conteúdo em *chunks*;
- Gerar embeddings utilizando Sentence Transformers;
- Criar ou atualizar o índice no Pinecone;
- Recuperar documentos relevantes utilizando busca vetorial MMR.

---

### 📄 chains.py

Implementa toda a lógica de Inteligência Artificial.

Neste arquivo são definidos:

- Modelo de Linguagem (LLM);
- Router Chain;
- Itinerary Chain;
- Local Info Chain;
- Logistics Chain;
- Translation Chain.

Também contém a função responsável por direcionar automaticamente cada consulta para a cadeia especializada.

---

### 📄 main.py

Interface principal do sistema.

Suas responsabilidades são:

- Inicializar a aplicação;
- Garantir que a Base de Conhecimento esteja indexada;
- Exibir o menu ao usuário;
- Receber perguntas;
- Exibir as respostas geradas.

---

### 📄 requirements.txt

Lista todas as bibliotecas utilizadas pelo projeto.

---

### 📄 .env.example

Modelo utilizado para configuração das variáveis de ambiente.

---

# ⚙️ Pré-requisitos

Antes de executar o projeto é necessário possuir:

- Python 3.10 ou superior;
- Conta na Groq;
- Conta no Pinecone.

---

# 🔑 Obtendo as Chaves de API

## Groq

Criar uma conta em:

https://console.groq.com/

Gerar uma chave de API.

---

## Pinecone

Criar uma conta em:

https://app.pinecone.io/

Criar um índice e gerar uma chave de API.

---

# 🚀 Instalação

## 1. Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/AIgente-Turistico.git

cd AIgente-Turistico
```

---

## 2. Criar o ambiente virtual

### Windows

```bash
python -m venv venv
```

### Linux / macOS

```bash
python3 -m venv venv
```

---

## 3. Ativar o ambiente virtual

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

Caso utilize a versão mais recente do LangChain, recomenda-se instalar também:

```bash
pip install -U langchain-huggingface
```

---

# 🔐 Configuração do arquivo .env

Crie um arquivo chamado:

```text
.env
```

na raiz do projeto contendo:

```env
GROQ_API_KEY="SUA_CHAVE_GROQ"

PINECONE_API_KEY="SUA_CHAVE_PINECONE"

PINECONE_INDEX_NAME="aigente-turistico"
```

---

# ▶️ Executando o Sistema

Basta executar:

```bash
python main.py
```

Durante a inicialização, o sistema executará automaticamente as seguintes etapas:

1. Verifica se o índice existe no Pinecone.

2. Atualiza a Base de Conhecimento.

3. Gera os embeddings.

4. Indexa os documentos.

5. Inicializa o Modelo de Linguagem.

6. Inicia a interface de linha de comando.

Após isso, basta realizar perguntas ao sistema.

---

# 🧠 Como o Sistema Funciona

O processamento ocorre em quatro etapas principais.

## 1. Classificação

A Router Chain identifica automaticamente a intenção da consulta.

Exemplo:

```text
"Monte um roteiro de 3 dias em Paris."
```

↓

```text
Itinerary Chain
```

---

```text
"Quais são os restaurantes veganos do Rio?"
```

↓

```text
Local Info Chain
```

---

```text
"Como ir do aeroporto Charles de Gaulle ao centro?"
```

↓

```text
Logistics Chain
```

---

```text
"Como dizer 'Obrigado' em francês?"
```

↓

```text
Translation Chain
```

---

## 2. Recuperação do Contexto

As Chains que utilizam RAG realizam uma busca vetorial no Pinecone.

O Retriever recupera os documentos mais relevantes utilizando o algoritmo **MMR (Maximal Marginal Relevance)**.

---

## 3. Geração da Resposta

O contexto recuperado é enviado ao modelo Qwen juntamente com a pergunta do usuário.

O modelo gera uma resposta contextualizada e organizada.

---

## 4. Exibição

A resposta é apresentada diretamente no terminal para o usuário.

---

# 💬 Exemplos de Utilização

Após iniciar o sistema, basta digitar uma pergunta.

Exemplo:

```text
✈️ Digite sua pergunta sobre a viagem:

Monte um roteiro de 3 dias em Paris.
```

Resposta esperada:

```text
Dia 1

- Torre Eiffel
- Champ de Mars
- Cruzeiro pelo Rio Sena

Dia 2

- Museu do Louvre
- Jardin des Tuileries
- Catedral de Notre-Dame

Dia 3

- Montmartre
- Basílica de Sacré-Cœur
- Café de Flore
```

---

Outro exemplo:

```text
Quais são os restaurantes veganos do Rio de Janeiro?
```

Resposta:

```text
Restaurantes Veganos no Rio de Janeiro

• Teva
  - Bairro: Ipanema
  - Gastronomia vegetal sofisticada.

• Prana Vegetariano
  - Bairro: Jardim Botânico

• Spaghetlandia
  - Especializada em massas.
```

---

Outro exemplo:

```text
Como ir do aeroporto Charles de Gaulle ao centro de Paris?
```

Resposta:

```text
A forma mais recomendada é utilizar o trem RER B.

• Tempo médio:
35 a 45 minutos.

• Destino:
Estação Châtelet–Les Halles.

Também é possível utilizar táxis e serviços por aplicativo.
```

---

Outro exemplo:

```text
Como dizer "Obrigado" em francês?
```

Resposta:

```text
Tradução:
Merci.

Pronúncia:
Mêr-si.

Exemplo:

Merci pour votre aide.

(Obrigado pela sua ajuda.)
```

---

# 🔍 Funcionamento do RAG

O sistema utiliza a técnica **Retrieval-Augmented Generation (RAG)** para responder perguntas específicas sobre os destinos cadastrados.

O processo ocorre da seguinte forma:

1. O usuário envia uma pergunta.

2. O Retriever realiza uma busca vetorial utilizando o Pinecone.

3. Os documentos mais relevantes são recuperados.

4. Esses documentos são enviados como contexto para o Modelo de Linguagem.

5. O modelo gera uma resposta baseada no contexto encontrado.

Essa abordagem reduz alucinações e aumenta a precisão das respostas.

---

# 🧠 Router Chain

Antes de responder, o sistema identifica automaticamente a intenção da pergunta.

As categorias disponíveis são:

| Categoria | Responsabilidade |
|------------|------------------|
| Itinerary Chain | Criação de roteiros personalizados |
| Local Info Chain | Informações turísticas utilizando RAG |
| Logistics Chain | Transporte e logística utilizando RAG |
| Translation Chain | Traduções para viagens |

Essa estratégia evita que um único prompt tente resolver todos os tipos de consulta.

---

# ⚡ Melhorias Implementadas

Durante o desenvolvimento foram implementadas diversas melhorias na arquitetura do sistema.

## Inteligência Artificial

- Router Chain para classificação automática.
- Cadeias especializadas por domínio.
- Integração com o modelo Qwen 3.8-27B.
- Prompts especializados para cada tipo de consulta.

---

## RAG

- Base de conhecimento em arquivos TXT.
- Indexação automática.
- Embeddings utilizando Sentence Transformers.
- Busca vetorial com Pinecone.
- Retriever utilizando algoritmo MMR.

---

## Arquitetura

- Separação em módulos independentes.
- Código organizado em Chains.
- Inicialização automática do banco vetorial.
- Atualização automática da Base de Conhecimento.

---

## Interface

- Interface em linha de comando.
- Mensagens organizadas.
- Tratamento de erros.
- Menu interativo.

---

# 🚀 Possíveis Trabalhos Futuros

O projeto pode ser expandido com diversas funcionalidades.

Entre elas:

- Inclusão de novos destinos turísticos.
- Integração com APIs de clima.
- Consulta de hotéis.
- Consulta de voos.
- Planejamento financeiro da viagem.
- Geração de mapas interativos.
- Interface Web utilizando Streamlit.
- Interface Web utilizando Flask.
- Aplicação Mobile.
- Histórico de conversas.
- Memória Conversacional.
- Integração com WhatsApp.
- Geração de PDFs contendo roteiros completos.

---

# 📊 Resultados Obtidos

O sistema foi capaz de:

- Classificar automaticamente diferentes tipos de perguntas.
- Recuperar informações utilizando RAG.
- Gerar roteiros personalizados.
- Responder perguntas sobre transporte.
- Informar atrações turísticas.
- Traduzir frases úteis para turistas.

A arquitetura modular também facilita a manutenção e futuras expansões do projeto.

---

# 📚 Referências

- LangChain Documentation

https://python.langchain.com/

---

- Groq Documentation

https://console.groq.com/docs

---

- Pinecone Documentation

https://docs.pinecone.io/

---

- Sentence Transformers

https://www.sbert.net/

---

# 👨‍💻 Autor

Projeto desenvolvido como atividade da disciplina de **Inteligência Artificial na Prática**, com foco na aplicação de Grandes Modelos de Linguagem (LLMs), Retrieval-Augmented Generation (RAG) e bancos de dados vetoriais para construção de assistentes inteligentes.

---

# 📄 Licença

Este projeto possui finalidade exclusivamente acadêmica e educacional.

Seu uso é livre para fins de estudo, pesquisa e aprendizado.

---

# ⭐ Considerações Finais

O AIgente-Turístico demonstra como combinar **Modelos de Linguagem**, **RAG**, **Router Chains** e **Bancos Vetoriais** para construir um assistente inteligente especializado.

A arquitetura proposta é modular, escalável e pode ser facilmente adaptada para outros domínios, como saúde, educação, atendimento ao cliente e suporte técnico, bastando substituir a Base de Conhecimento e ajustar os prompts especializados.

Esse projeto também evidencia a importância da separação de responsabilidades entre os módulos de classificação, recuperação de contexto e geração de respostas, proporcionando maior organização, reutilização de código e facilidade de manutenção.
