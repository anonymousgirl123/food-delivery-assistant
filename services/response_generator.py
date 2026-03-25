def generate_response(recommendations):
    return "Recommended: " + ", ".join([r["name"] for r in recommendations])
