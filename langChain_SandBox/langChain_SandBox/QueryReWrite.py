from openai import OpenAI
client = OpenAI()

def rewrite_query(original_query: str) -> str:
    prompt = f"Rewrite the following query to improve its clarity and specificity for improved retrieval: \n\n'{original_query}'"
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    rewritten_query = response.choices[0].message.content
    return rewritten_query