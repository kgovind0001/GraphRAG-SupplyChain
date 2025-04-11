# GraphRAG: Graph-Based Retrieval-Augmented Generation using Neo4j

<p align="center">
  <img src="assets/demo.gif" alt="GraphRAG Demo" width="600"/>
</p>

This is a Python-based application that combines the strengths of knowledge graphs and vector databases to enhance Retrieval-Augmented Generation (RAG) systems. By leveraging Neo4j for graph storage and OpenAI's language models, GraphRAG provides structured, context-rich responses to complex queries.

---

## 🚀 Features

- **Graph-Enhanced Retrieval**:Utilizes Neo4j to store and query knowledge graphs, capturing intricate relationships between data entities
- **Vector Similarity Search**:Integrates vector databases for efficient similarity-based retrieval
- **OpenAI Integration**:Employs OpenAI's language models for generating coherent and context-aware responses
- **Modular Architecture**:Designed with modularity in mind, allowing easy customization and extension

---

## 🧰 Prerequisites

 1. Python 3.9
 2. Docker & Docker Compose 
 3. [pyenv](https://github.com/pyenv/pyenv) & [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
 4. OpenAI API Ky

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/kgovind0001/GraphRAG-SupplyChain.git
cd GraphRAG-SupplyChain
```


### 2. Configure Environment Variables
Create a `.env` file in the root directory and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
NEO4J_URI="neo4j://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "password"
```


### 3. Set Up Python Environment
Use `pyenv` and `pyenv-virtualenv` to create and activate a Python 3.9.0 environment:

```bash
pyenv install 3.9.0
pyenv virtualenv 3.9.0 graphrag-env
pyenv activate graphrag-env
```


### 4. Install Dependencies
Install the required Python package:

```bash
pip install -r requirements.txt
```


### 5. Launch Neo4j with Docker
Ensure Docker and Docker Compose are installed, then start the Neo4j server:

```bash
docker-compose up -d
```

This will set up a Neo4j instance with the necessary plugins for vectorized storage and OpenAI integration.

### 6. Run the Application
Start the GraphRAG applicatio:

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```plaintext
GraphRAG-SupplyChain/
├── sample_data/               # Input data files
├── src/                                 # Source code
    ├── __init__.py
    ├── models                           # Pydantic models
    │   ├── __init__.py
    │   ├── models.py
    ├── supply_chain_assistant.py        # Core RAG pipeline implementation
    └── tools                            # Functions for graph operations
        ├── __init__.py
        ├── supply_count.py
        └── supply_list.py
├── .env                # Environment variables
├── requirements.txt    # Python dependencies
├── app.py    # Streamlit application
└── docker-compose.yml  # Docker Compose configuration
```

---

## 🧪 Testing the Setup

After running the application, you can test its functionality by:
1. Adding sample data to the `sample_data/` directory.
2. Ensuring the data is ingested and processed correctly.
3. Submitting queries and verifying the responses are accurate and contextually relevent.

---

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.
---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/kgovind0001/GraphRAG-SupplyChain/blob/main/LICENSE) file for details.

---

## 🙌 Acknowledgents

Developed by [Kishan Govind](https://github.com/kgovind0001).
Huge Thanks to [medium post](https://medium.com/globant/langgraph-ai-agents-with-neo4j-knowledge-graph-7e688888f547) for the motivation. 

---

Feel free to customize this README further to match your project's specific details and requirements. 