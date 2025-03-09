import requests
import json
import secret


def back(message):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {secret.token_gpt}", "Content-Type": "application/json"},
        
        data=json.dumps({
            "model": "google/gemini-2.0-pro-exp-02-05:free",
            "messages": [
                {"role": "system", "content": [ {"type": "text", "text": "Ты умный бот, помогающий пользователям и отвечающий только по русски(RU)"} ] },
                {"role": "user", "content": [{"type": "text", "text": message}] }
            ],
            "max_tokens": 1000
        })
    )
        
    return json.loads(json.dumps(response.text))

def ask(message):
    try:
        shit = json.loads(back(message))
        message_content = shit['choices'][0]['message']['content']

        return message_content

    except KeyError:
        shit = json.loads(back(message))
        message_content = shit['choices'][0]['message']['content']

        return message_content

    except Exception as e:
        return e
