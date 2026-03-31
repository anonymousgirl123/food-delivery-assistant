def generate_ai_explanation(food, context, user):
    prompt = f"""
    Explain why this food is recommended.

    Food: {food['name']}
    Context: {context}
    User Preferences: {user}

    Keep it short and natural.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message["content"]

# def generate_response(recommendations):
#     replies = []

#     for food in recommendations:
#         explanation = generate_ai_explanation(food, {}, {})
#         replies.append(f"{food['name']} → {explanation}")

#     return replies


import openai

def generate_chat_response(recommendations, intent, context, user):
    prompt = f"""
    You are a smart food assistant.

    User intent:
    {intent}

    Context:
    {context}

    Recommendations:
    {recommendations}

    Generate a friendly, conversational response.
    Suggest 2-3 items with short explanations.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message["content"]
    
