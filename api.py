# 1. Obtain or create your Open WebUI API key

 

# [User Name] > Settings > Account > API keys in the Open WebUI

 

# 2. Create python script

 

# $ cat chat.py

#!/usr/bin/python

import sys

import requests

 

def chat_with_model(token,model,question):

    url = 'https://idun-llm.hpc.ntnu.no/api/chat/completions'

    headers = {

        'Authorization': f'Bearer {token}',

        'Content-Type': 'application/json'

    }

    data = {

      "model": model,

      "messages": [

        {

          "role": "user",

          "content": question

        }

      ]

    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()

 

my_api_key = sys.argv[1]

my_model = sys.argv[2]

my_question = sys.argv[3]

answer = chat_with_model(my_api_key, my_model, my_question)

print(answer)

 

# 3. Use

 

# $ python3 chat.py 'MY-API-KEY' 'llama3.2:1b' 'Why sky is blue?'