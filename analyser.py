def calculate_visibility_score(rank, ai_present):
    """
    Calculates brand visibility score based on rank tier and AI presence.
    """
    score = 0.0
    
    # Traditional ranking weight
    if rank == 1:
        score += 50.0
    elif rank <= 3:
        score += 35.0
    elif rank <= 10:
        score += 20.0
    elif rank <= 20:
        score += 5.0
        
    # AI Search feature bonus weight
    if ai_present:
        score += 50.0
        
    return score