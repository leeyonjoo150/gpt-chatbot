#ai로 하여금 질문 내용에 따라서 고급인지 아닌지 판단하면 됩니다.from openai import OpenAI
from openai import OpenAI
import os
import json
from datetime import date
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ai_routing(question) :
    messages = [{"role" : "system",
                 "content" : "너는 질문 내용에 따라서 고급인지 아닌지 판단하는 역할을 해. 고급인지 아닌지 판단하고 그 결과를 '고급' 또는 '심플'로 반환해. 그리고 그렇게 판단한 이유도 같이 설명해."}]
    messages.append({"role" : "user", "content" : question})
    response = client.chat.completions.create(model="gpt-4o-mini", messages=messages, temperature=1)
    return response.choices[0].message.content

#output = ai_routing("나는 중학생이야. 나는 중학생 국어 학습을 열심히 하고 싶어. 나는 중학생 국어 학습을 열심히 하고 싶어.")
#output = ai_routing("한국의 AI산업의 발전을 위해서 정부의 각 부처에서 준비하고 실행해야 할 내용을 정리해줘")
output = ai_routing("f(x) x^2 + 2x + 1 의 도함수를 알려줘.")
print(output)

if output == "고급" :
    model = "gpt-5o"
else :
    model = "gpt-4o-mini"