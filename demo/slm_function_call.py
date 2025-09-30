from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = """
너는 사용자에게 도움이 되는 정보를 제공하는 역할을 해.
그런데, 외부 도구를 이용하려면
{"name" : 도구이름, "args" : {매개변수1 : 값1, 매개변수2 : 값2}}
형식으로 응답하면 돼.
네가 쓸 수 있는 도구는
{get_current_time() : 현재 시간을 알 수 있음}
"""

user_prompt = "지금 몇시야?"
response = client.chat.completions.create(
        model=os.getenv("OLLAMA_MODEL"),
        messages=[
            {"role" : "system", "content" : system_prompt},
            #{"role" "user", "content" : user_prompt}
        ]
    )

print(response.choices[0].message.content)