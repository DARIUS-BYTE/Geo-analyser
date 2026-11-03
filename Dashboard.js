async function runTracker() {
    const keyword = document.getElementById('keyword').value;
    const brand = document.getElementById('brand').value;

    if (!keyword || !brand) {
        alert('Please enter both keyword and brand name.');
        return;
    }

    const res = await fetch('/api/track', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ keyword, brand })
    });
    const result = await res.json();
    
    alert(`LangGraph Agent Execution Complete!\nRank: ${result.rank}\nAI Overview: ${result.ai_present}\nScore: ${result.visibility_score}\n\nInsights: ${result.insights}`);
    loadData();
}