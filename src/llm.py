"""import os
from openai import OpenAI

API_KEY = "aa-Dn7aKjkWDftS2xnkBmIkVwylPGpQNC56u0CdAgj1gWYYLPXD"
BASE_URL = "https://api.avalai.ir/v1"

# تنظیم کلید و آدرس
client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # مدل AvalAI
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "سلام! ما روی چه سیاره ای زندگی میکنم ؟"}
        ]
    )
    print("Python Response:", response.choices[0].message.content)

except Exception as e:
    print("Python Error:", e)"""

import os
from openai import OpenAI

API_KEY = "aa-Dn7aKjkWDftS2xnkBmIkVwylPGpQNC56u0CdAgj1gWYYLPXD"
BASE_URL = "https://api.avalai.ir/v1"

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)

def call_llm(prompt, model="gpt-4o-mini", system_prompt="You are a helpful and funny English teacher assistant. You have to talk just english ."):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        raise e  # or handle/log as needed