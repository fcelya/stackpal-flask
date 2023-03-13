import os
from dotenv import load_dotenv
from pathlib import Path
import requests
import securepy
import time

def load_env():
    try:
        dotenv_path = Path("../.flaskenv")
        load_dotenv(dotenv_path = dotenv_path)
    except:
        try:
            dotenv_path = Path("./.flaskenv")
            load_dotenv(dotenv_path = dotenv_path)
        except:
            pass

def openai_request_code(code,language="Python"):
    KEY = os.getenv("OPEN_AI_API_KEY")
    MODEL = "gpt-3.5-turbo"
    URL = "https://api.openai.com/v1/chat/completions"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer "+KEY
    }

    messages = [
        {"role":"system", "content": f"You are a code optimization assistant. I am going to provide you with {language} code. You will provide a faster version of that code that will retain the same functionality, but will do it faster and more efficiently."},
        {"role":"user", "content":code}
    ]

    data = {"model":MODEL,
            "messages":messages}

    r = requests.post(url=URL,headers=headers,json=data)

    return r.json()

def test_module():
    print("fuck your test")

def time_code(code,security=2,max_time = 30):
    restrictor = securepy.Restrictor(max_exec_time=max_time, restriction_scope=security)
    start_time = time.time()
    stdout, exc = restrictor.execute(code)
    print(exc)
    end_time = time.time()
    return end_time - start_time