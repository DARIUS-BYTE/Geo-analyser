from flask import Flask, render_template, jsonify, request
from database import init_db, save_ranking, get_all_rankings
from agent_workflow import run_seo_agent, kb

app = Flask(__name__)
init_db()

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/data')
def get_data():
    rows = get_all_rankings()
    data = [{
        "keyword": r[0],
        "brand": r[1],
        "rank": r[2],
        "ai_present": bool(r[3]),
        "timestamp": r[4]
    } for r in rows]
    return jsonify(data)

@app.route('/api/track', methods=['POST'])
def trigger_track():
    req_data = request.json
    keyword = req_data.get('keyword')
    brand = req_data.get('brand')
    
    if not keyword or not brand:
        return jsonify({"error": "Keyword and brand required"}), 400
        
    # Execute via LangGraph Workflow (Scraping -> RAG -> Analysis)
    result = run_seo_agent(keyword, brand)
    
    # Save to SQLite database
    save_ranking(keyword, brand, result['rank'], result['ai_present'])
    
    return jsonify({
        "status": "success",
        "keyword": keyword,
        "brand": brand,
        "rank": result['rank'],
        "ai_present": result['ai_present'],
        "visibility_score": result['visibility_score'],
        "insights": result['insights']
    })

@app.route('/api/add_knowledge', methods=['POST'])
def add_knowledge():
    """Allows adding custom SEO guidelines into the local RAG store"""
    req_data = request.json
    text = req_data.get('text')
    if text:
        kb.add_document(text)
        return jsonify({"status": "success", "message": "Knowledge added to RAG index."})
    return jsonify({"error": "Text required"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)