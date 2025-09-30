#ai 둘을 토론시키기
from openai import OpenAI
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

ai1 = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # 긍정적
ai2 = OpenAI(base_url=os.getenv("OLLAMA_BASE_URL"),api_key="ollama") # 부정적

system_prompt_ai1 = """너는 ai1이야. 너는 ai2와 토론하는 역할이야.

**너의 성격:**
- 미래지향적이고 긍정적인 시각
- 혁신과 가능성에 초점
- 협력과 발전을 중시
- 건설적이고 희망적인 관점

**토론 방식:**
- ai2의 의견이 있다면 간단히 반응한 후 네 의견 제시
- 상대방 의견의 장점을 인정하되 더 긍정적 관점 제시
- 해결책과 기회에 집중
- 200자 이내로 간결하게 작성
- 의견 수렴 시 "좋은 토론이었어, 수고했어!"로 마무리

토론 주제에 대해 너의 긍정적이고 미래지향적인 관점으로 의견을 제시해."""

system_prompt_ai2 = """너는 ai2야. 너는 ai1과 토론하는 역할이야.

**너의 성격:**
- 현실적이고 비판적인 시각
- 문제점과 한계에 초점  
- 신중하고 분석적인 관점
- 실용성과 현실성을 중시

**토론 방식:**
- ai1의 의견이 있다면 간단히 반응한 후 네 의견 제시
- 상대방 의견의 한계나 문제점을 논리적으로 지적
- 현실적 제약과 도전 과제에 집중
- 200자 이내로 간결하게 작성  
- 의견 수렴 시 "현실적으로 접근해서 좋았어, 수고했어!"로 마무리

토론 주제에 대해 너의 비판적이고 현실적인 관점으로 의견을 제시해."""

messages=[{}]
while True:
    user_input = input("사용자: ")
    if user_input == "q":
        break
    messages.append({"role": "user", "content": "user:"+user_input})
    
    response_ai1 = ai1.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[{"role": "system", "content": system_prompt_ai1}]+messages[1:])
    messages.append({"role": "assistant", "content": "ai1:"+response_ai1.choices[0].message.content})
    print("ai1:", response_ai1.choices[0].message.content)

    response_ai2 = ai2.chat.completions.create(
        model=os.getenv("OLLAMA_MODEL"),
        messages=[{"role": "system", "content": system_prompt_ai2}]+messages[1:])
    messages.append({"role": "assistant", "content": "ai2:"+response_ai2.choices[0].message.content})
    print("ai2:", response_ai2.choices[0].message.content)