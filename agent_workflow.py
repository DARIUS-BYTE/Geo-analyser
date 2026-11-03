import operator
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from scraper import scrape_serp_and_ai
from analyzer import calculate_visibility_score
from rag_engine import LocalSEOKnowledgeBase

# Define the shared execution state schema
class SEOState(TypedDict):
    keyword: str
    brand: str
    rank: int
    ai_present: bool
    visibility_score: float
    rag_context: list[str]
    insights: str

# Instantiate our local RAG knowledge base
kb = LocalSEOKnowledgeBase()

# Node 1: Scrape SERP & AI features
def node_scrape(state: SEOState) -> dict:
    print(f"--- [LangGraph] Scraping SERP for: {state['keyword']} ---")
    result = scrape_serp_and_ai(state['keyword'], state['brand'])
    return {"rank": result["rank"], "ai_present": result["ai_present"]}

# Node 2: Retrieve Context using RAG
def node_retrieve_rag(state: SEOState) -> dict:
    print(f"--- [LangGraph] Fetching RAG context for keyword ---")
    query = f"SEO ranking factors for {state['keyword']} with AI Overview presence {state['ai_present']}"
    context = kb.search(query, k=2)
    return {"rag_context": context}

# Node 3: Calculate score & generate analytical feedback
def node_analyze(state: SEOState) -> dict:
    print(f"--- [LangGraph] Calculating score & synthesizing insights ---")
    score = calculate_visibility_score(state['rank'], state['ai_present'])
    
    # Synthesize insights combining score and retrieved RAG context
    context_str = " ".join(state['rag_context'])
    insights = f"Ranked #{state['rank']} organically. AI Overview inclusion is {state['ai_present']}. Visibility Score: {score}/100. Context analysis: {context_str}"
    
    return {"visibility_score": score, "insights": insights}

# Build the LangGraph Workflow Graph
workflow = StateGraph(SEOState)

workflow.add_node("scrape_node", node_scrape)
workflow.add_node("rag_node", node_retrieve_rag)
workflow.add_node("analyze_node", node_analyze)

# Define sequential execution edges
workflow.add_edge(START, "scrape_node")
workflow.add_edge("scrape_node", "rag_node")
workflow.add_edge("rag_node", "analyze_node")
workflow.add_edge("analyze_node", END)

# Compile graph into an executable runner
seo_graph = workflow.compile()

def run_seo_agent(keyword: str, brand: str) -> dict:
    initial_state = {
        "keyword": keyword,
        "brand": brand,
        "rank": 99,
        "ai_present": False,
        "visibility_score": 0.0,
        "rag_context": [],
        "insights": ""
    }
    final_state = seo_graph.invoke(initial_state)
    return final_state