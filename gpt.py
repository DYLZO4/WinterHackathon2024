import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
client = OpenAI(
    api_key=os.environ.get('OPEN_AI_KEY')
)
model = "gpt-3.5-turbo"
temperature = 1.5
max_tokens = 50
topic = ""

messages = [
    {"role": "system", "content": "You are a productivity assistant."},
    {"role": "user", "content": "give me motivation to stay focused in 10 words or less. Be harsh but do not cuss"}
]

def get_motivation():
    completion = client.chat.completions.create(
        model = model,
        messages= messages,
        temperature= temperature,
        max_tokens= max_tokens
    )
    return print(completion.choices[0].message.content)