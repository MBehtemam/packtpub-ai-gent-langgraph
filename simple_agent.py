import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv();

openai_key = os.getenv("OPENAI_API_KEY")

llm_name = "gpt-3.5-turbo"

client = OpenAI(api_key=openai_key)

response = client.chat.completions.create(
    model=llm_name,
    messages=[
        { "role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content":"Who is Nelson Mandela?"}
    ]
)

print(response.choices[0].message.content)