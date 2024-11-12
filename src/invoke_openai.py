import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv('.env')

client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY"),
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "你是一个诗意的助手"},
    {"role": "user", "content": "3+4"}
  ]
)
def invoke_openai():
  print(completion.choices[0].message)