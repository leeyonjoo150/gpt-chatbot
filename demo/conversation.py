# conversation.py
from openai import OpenAI
import os
from dotenv import load_dotenv
#from prompts import OPUS_SYSTEM_PROMPT

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_ai():
    """AI와 대화하기"""

    # 대화 기록 저장
    messages = [
        {"role": "system", "content": "당신은 친절한 학습 도우미입니다."}
    ]

    print("AI 도우미: 안녕하세요! 무엇이 궁금하신가요?")
    print("(종료하려면 'quit' 입력)")
    print("-" * 50)

    while True:
        # 사용자 입력
        user_input = input("나: ")

        # 종료 조건
        if user_input.lower() == 'quit':
            print("AI 도우미: 안녕히 가세요!")
            break

        # 사용자 메시지 추가
        messages.append({"role": "user", "content": user_input})

        # AI 응답 생성
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        # AI 응답 추출
        ai_message = response.choices[0].message.content

        # AI 메시지 기록
        messages.append({"role": "assistant", "content": ai_message})

        # 응답 출력
        print(f"AI 도우미: {ai_message}")
        print("-" * 50)

# 실행
if __name__ == "__main__":
    chat_with_ai()


#클로드한테 물어봐서 적용해보기 해봐도 좋을 듯
#chatgpt를 쓰면 내부적으로 messages가 누적되어 토큰이나 성능에 영향을 미쳐. 그런데 맥락을 이해하며 대화하려면 필수적이라고 생각해. 그런데 이런 messages를 최적화 할 수 있는 방법이 있을까?
#https://claude.ai/share/e7434970-c922-48df-ae41-7ed039c6049e