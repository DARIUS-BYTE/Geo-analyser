# Geo Analyser

**Geo Analyser** is an agentic, zero-cost, CPU-optimized AI Visibility & SEO Analytics Platform built with **Python**, **LangChain**, **LangGraph**, **RAG (FAISS)**, and **Playwright**. This platform tracks, scores, and analyzes brand visibility across traditional Search Engine Result Pages (SERPs) and AI-powered search features (such as Google AI Overviews and Bing Copilot).

## Key Features

* **Agentic Workflow Engine:** Uses **LangGraph** to execute a deterministic 3-stage agent pipeline (`Scrape` $\rightarrow$ `RAG Context Retrieval` $\rightarrow$ `Score & Insights Generation`).

* **Dynamic SERP Scraping:** Leverages **Playwright** and **BeautifulSoup** to render dynamic JavaScript blocks and detect brand mentions within AI Overviews and organic search rankings.

* **Local RAG Integration:** Employs **FAISS** and **HuggingFace Embeddings** (`all-MiniLM-L6-v2`) to query internal brand guidelines and benchmark notes locally without external API dependencies.

* **Lightweight Storage:** Utilizes **SQLite** for zero-configuration, CPU-friendly data persistence.

* **Interactive Visualizations:** Provides a clean **Flask** backend with a responsive **Chart.js** frontend dashboard for tracking rank positioning and AI presence rates over time.

## Tech Stack

* **Language:** Python 3.9+

* **Agentic Framework:** LangGraph, LangChain

* **Vector Database & RAG:** FAISS (CPU), HuggingFace Sentence Transformers

* **Scraping & Automation:** Playwright, BeautifulSoup4

* **Backend Framework:** Flask

* **Database:** SQLite3

* **Frontend & Charting:** HTML5/CSS3, JavaScript, Chart.js

## Project Structure

```
geo_analyser/
│
├── database.py         # SQLite database schema and helper queries
├── scraper.py          # Playwright dynamic web scraping pipeline
├── analyzer.py         # Quantitative visibility scoring engine
├── rag_engine.py       # Local FAISS vector index & embedding pipeline
├── agent_workflow.py   # LangGraph agent orchestration state graph
├── app.py              # Flask web app and REST API entrypoint
└── templates/
    └── dashboard.html  # Interactive Chart.js dashboard

```

## Installation & Setup

### 1. Prerequisites

Ensure you have Python 3.9+ installed on your system.

### 2. Clone the Repository & Set Up Virtual Environment

```
git clone https://github.com/your-username/geo-analyser.git
cd geo-analyser

python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

```

### 3. Install Dependencies

Install all required Python packages and browser binaries:

```
pip install flask playwright beautifulsoup4 requests langchain langchain-community langgraph faiss-cpu sentence-transformers
playwright install chromium

```

## Running the Application

1. **Launch the Flask Server:**

   ```
   python app.py
   
   ```

2. **Access the Web Dashboard:**
   Open your browser and navigate to `http://127.0.0.1:5000`.

## API Endpoints

| Method | Endpoint | Description | 
| ----- | ----- | ----- | 
| `GET` | `/` | Renders the primary analytics dashboard UI. | 
| `GET` | `/api/data` | Fetches all recorded keyword rankings and AI presence logs. | 
| `POST` | `/api/track` | Triggers the LangGraph agent for a target `keyword` and `brand`. | 
| `POST` | `/api/add_knowledge` | Adds new custom rules or brand context to the local FAISS index. | 

## Visibility Scoring Methodology

The overall Visibility Score ($V$) combines organic positioning with AI search feature inclusion:

$$
V = \text{Organic Rank Score} + \text{AI Presence Bonus}
$$

* **Organic Position Tiers:**

  * Rank 1: **50 pts**

  * Rank 2–3: **35 pts**

  * Rank 4–10: **20 pts**

  * Rank 11–20: **5 pts**

* **AI Feature Inclusion Bonus:** **+50 pts** if the brand is cited in AI Overviews / Copilot.

## License

This project is licensed under the MIT License.
