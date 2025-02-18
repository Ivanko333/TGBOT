from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)


def ask_gpt(message):
    completion = client.chat.completions.create(
        model="google/gemini-2.0-flash-exp:free",
        messages=[
            {
                "role": "user",
                "content": message
            }
        ]
    )
    return completion.choices[0].message.content