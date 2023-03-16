import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
import sys, traceback, logger
import requests
import securepy
from time import time
from re import findall

def load_env():
    try:
        dotenv_path = Path("../.flaskenv")
        load_dotenv(dotenv_path = dotenv_path)
    except:
        print("WARNING: Load env 1 failed")
        try:
            dotenv_path = Path("./.flaskenv")
            load_dotenv(dotenv_path = dotenv_path)
        except:
            print("WARNING: Load env 2 failed")
            try:
                load_dotenv()
            except:
                print("ERROR: Load env 3 failed")
                pass

def openai_request_code(code,language="Python",temperature = 0.6):
    KEY = os.getenv("OPEN_AI_API_KEY")
    MODEL = "gpt-3.5-turbo"
    URL = "https://api.openai.com/v1/chat/completions"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer "+KEY
    }

    messages = [
        {"role":"system", "content": f"You are a code optimization assistant. I am going to provide you with {language} code. You will provide a faster and more efficient version of that code that will retain the same functionality. Your answer should start directly with the optimized code, and be followed by an explanation of the changes."},
        {"role":"user", "content":code}
    ]

    data = {"model":MODEL,
            "messages":messages,
            "temperature":temperature}

    r = requests.post(url=URL,headers=headers,json=data)
    data = r.json()

    response = {}
    response["id_answer"] = data["id"]
    response["answer_code"],response["answer_explanation"] = parse_answers(data["choices"][0]["message"]["content"])
    response["model"] = data["model"]
    response["tokens_prompt"] = data["usage"]["prompt_tokens"]
    response["tokens_response"] = data["usage"]["completion_tokens"]
    response["tokens_total"] = data["usage"]["total_tokens"]

    return response

def openai_request_code_test(code,language="Python"):
    MODEL = "gpt-3.5-turbo"
    response = {}
    response["id_answer"] = 'chatcmpl-6tas4m95wEC26nc1hjUQOzDdEOkbT'
    response["answer_code"],response["answer_explanation"] = "print('fuck yo mama')","fuck her cos she a hoe"
    response["model"] = MODEL
    response["tokens_prompt"] = 69
    response["tokens_response"] = 420
    response["tokens_total"] = 489

    return response


def test_module():
    print("fuck your test")

def time_code(code,security=2,max_time = 30):
    restrictor = securepy.Restrictor(max_exec_time=max_time, restriction_scope=security)
    start_time = time()
    stdout, exc = restrictor.execute(code)
    print(exc)
    end_time = time()
    return end_time - start_time

def parse_answers(answer):
    paragraphs = answer.split(f'\n\n')
    if len(paragraphs) == 2:
        return paragraphs
    scores = [paragraph_tokenizer(paragraph) for paragraph in paragraphs]
    diff_scores = [scores[i-1]-scores[i] for i in range(1, len(scores))]
    last_code = diff_scores.index(max(diff_scores)) + 1
    code = f'\n\n'.join(paragraphs[:last_code])
    explanation = f'\n\n'.join(paragraphs[last_code:])
    return code, explanation

def paragraph_tokenizer(paragraph):
    regex = r"[\[\]\(\)\+\-\/\*\=\:\.\,\!\&]|\breturn\b"
    count = len(findall(regex, paragraph))
    return count/len(paragraph)

def log_error(request,e):
    p = Path("app","logs")
    with open(p.joinpath(f"log_{(int)(datetime.timestamp(datetime.now()))}.txt"),"w+") as f:
        f.write(request.path)
        f.write(f"\n\n-------REQUEST-------\n")
        try:
            data = request.json
        except:
            data = request.data
        f.write((str)(data))
        f.write(f"\n\n-------ERROR-------\n")
        ex_type, ex_value, ex_traceback = sys.exc_info()
        # Extract unformatter stack traces as tuples
        trace_back = traceback.extract_tb(ex_traceback)
        # Format stacktrace
        stack_trace = list()

        for trace in trace_back:
            stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))
        f.write((str)(e))
        f.write(f"\nException type : {ex_type.__name__}")
        f.write(f"\nException message : {ex_value}")
        f.write(f"\nStack trace : {stack_trace}")
        
        # f.write((str)(e))
    return
