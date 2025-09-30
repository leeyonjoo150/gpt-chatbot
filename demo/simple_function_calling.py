from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 1: 실제 함수 정의
def calculate(expression: str) -> float:
    """수식을 계산하는 함수"""
    try:
        # 안전한 계산을 위해 eval 대신 제한적 사용
        allowed_chars = "0123456789+-*/()., "
        if all(c in allowed_chars for c in expression):
            result = eval(expression)   #eval()은 보안이 취약해서 사용자한테 보여지면 안됨, 문자열로된 파이썬 코드를 실행하는 내장 함수
            return result
        else:
            return "유효하지 않은 수식입니다"
    except:
        return "계산 오류"

def get_current_time() -> str:
    """현재 시간을 반환하는 함수"""
    from datetime import datetime
    return datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분")

# Step 2: OpenAI에게 함수 설명
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "수학 계산을 수행합니다",
            "parameters": {
                "type": "object",   #매개변수는 객체 형태
                "properties": {     #각 매개변수 정의
                    "expression": {     #매개변수 이름
                        "type": "string",
                        "description": "계산할 수식 (예: 2+2, 10*5)"    #설명+예시
                    }
                },
                "required": ["expression"]  #필수 매개변수 목록
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "현재 시간을 가져옵니다",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

# Step 3: 대화 함수
def chat_with_functions(user_input: str):
    """Function Calling이 가능한 채팅"""

    messages = [
        {"role": "system", "content": "당신은 도움이 되는 AI 어시스턴트입니다."},
        {"role": "user", "content": user_input}
    ]

    # AI 응답 (함수 호출 여부 판단)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto"  # AI가 자동으로 판단
    )

    message = response.choices[0].message       #수업시간에 디버그모드로 확인, 여기가 관건

    # 함수 호출이 필요한 경우
    if message.tool_calls:
        print("🔧 AI가 도구를 사용합니다...")

        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print(f"  → {function_name} 호출: {arguments}")

            # 실제 함수 실행
            if function_name == "calculate":
                result = calculate(arguments["expression"])
            elif function_name == "get_current_time":
                result = get_current_time()
            else:
                result = "알 수 없는 함수"

            print(f"  → 결과: {result}")

            # 결과를 다시 AI에게 전달
            messages.append(message)  # AI의 함수 호출 요청
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

        # 최종 응답 생성
        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        return final_response.choices[0].message.content

    # 함수 호출이 필요 없는 경우
    else:
        return message.content

# 테스트
print("💬 질문: 1234 + 5678은 뭐야?")   #솔직히 llm에서 충분히 답변 가능. 펑션콜 안해도 되는 수준
print("🤖 답변:", chat_with_functions("1234 + 5678은 뭐야?"))
print()

print("💬 질문: 지금 몇 시야?")
print("🤖 답변:", chat_with_functions("지금 몇 시야?"))
print()

print("💬 질문: 안녕하세요")
print("🤖 답변:", chat_with_functions("안녕하세요"))

#1. simple_function_calling.py를 실행해서 function calling의 원리를 이해
#2. (옵션) slm에 적용 방법 고민
#3. 나만의 도구를 만들어서 function calling을 적용해보기