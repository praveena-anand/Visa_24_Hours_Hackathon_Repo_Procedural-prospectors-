def recommend_actions(explanation):
    actions = []

    text = explanation.lower()

    if "decline" in text:
        actions.append({
            "action": "Review authorization rules and retry logic",
            "impact": "Increase approval rates",
            "priority": "High"
        })

    if "settlement" in text or "delay" in text:
        actions.append({
            "action": "Optimize settlement batching for affected regions",
            "impact": "Reduce settlement delays",
            "priority": "Medium"
        })

    if not actions:
        actions.append({
            "action": "Continue monitoring network metrics",
            "impact": "No immediate operational risk",
            "priority": "Low"
        })

    return actions
