import os
import requests
import json
base_prompt = "You will have a single job, you need to identify wether the author in the reddit post I provide you is either a male or a female, you will respond with a single lowercase letter, f or m, f for female, m for male. For no reason should yo go above your single character, if unsure, default to male (m). Here is the post: "

def is_female(post):
    API_KEY = os.getenv("OPENAI_API_KEY")
    API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": base_prompt+post}],
        "temperature": 0.7
    }
    
    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        response_json = response.json()
        text_response = response_json["choices"][0]["message"]["content"]
        return text_response
    else:
        raise Exception(f"API request failed with status code: {response.status_code}")
    
