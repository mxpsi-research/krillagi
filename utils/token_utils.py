def estimate_tokens(text):
    # Simple estimate: 1 token ≈ 4 chars
    return max(1, len(text) // 4)
