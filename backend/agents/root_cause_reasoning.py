from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def explain_root_cause(query, context):
    prompt = f"""
You are a Visa network payment analyst.

You have access to BOTH authorization and settlement report insights.

Context:
{context}

User question:
{query}

Task:
1. Identify if the issue originated in authorization or settlement.
2. Explain how authorization behavior impacted settlement outcomes (if applicable).
3. Provide a clear cause → effect explanation.

Respond in concise business language.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content
