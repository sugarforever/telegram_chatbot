import requests
import json

url = "https://gateway.openai-cloud.com/v1/chat/completions"

def ask(question):
    payload = json.dumps({
      "messages": [
        {
          "role": "user",
          "content": question
        }
      ],
      "model": "spark-api",
      "max_tokens": None,
      "stream": False,
      "n": 1,
      "temperature": 0.7,
      "version": "v2.1"
    })
    headers = {
      'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()["choices"][0]["message"]["content"]
    except:
        return None

if __name__ == "__main__":
    answer = ask("李白最有名的诗是什么？")
    print(answer)