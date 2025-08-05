import re

def parse_command(text):
    text = text.lower().strip()

    # Exit command
    if any(x in text for x in ["exit", "quit", "close"]):
        return {"action": "exit"}

    # Show expenses
    if "show" in text and "expense" in text:
        return {"action": "show"}

    # Delete all expenses
    if any(phrase in text for phrase in ["delete all", "clear expenses", "remove all", "delete everything"]):
        return {"action": "delete_all"}

    # Add expense: e.g., "add 500 to groceries", "spent 500 on groceries", "groceries 500"
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:rupees|rs)?\s*(?:to|on|for|in)?\s*(\w+)', text)
    if match:
        amount = match.group(1)
        category = match.group(2)
        return {"action": "add", "amount": amount, "category": category}

    # Alternative add pattern: e.g., "add groceries 500"
    match_alt = re.search(r'(?:add|put)?\s*(\w+)\s*(\d+(?:\.\d+)?)', text)
    if match_alt:
        category = match_alt.group(1)
        amount = match_alt.group(2)
        return {"action": "add", "amount": amount, "category": category}

    return {"action": "unknown"}
