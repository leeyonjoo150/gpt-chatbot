# 1. 필요한 것들 가져오기
from openai import OpenAI
import os
from dotenv import load_dotenv

# 2. API 키 로드
load_dotenv()

# 3. OpenAI 클라이언트 생성
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 4. AI에게 인사하기
response = client.chat.completions.create(
    model="gpt-4o-mini",    #어떤 모델을 쓸 것인지, 사이트 들어가서 있는 모델 중 확인해서 이름 적으면 됨
    #messages를 리스트 안에 딕셔너리 형태로
    #role과 content 조합으로 저장
    messages=[
        {"role": "user", "content": "안녕하세요!"}
        #{"role": "user", "content": "한국의 대통령은 누구인가!"}
    ]
)

# 5. 응답 출력
print(response.choices[0].message.content)


# 예시: 역할별 차이
def test_roles():
    # 1. system 역할 없이
    response1 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "1+1은?"}
        ]
    )
    print("기본 응답:", response1.choices[0].message.content)

    # 2. system 역할 추가
    response2 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            #{"role": "system", "content": "당신은 5살 어리고 애교 많은 아이입니다."},
            #{"role": "system", "content": "당신은 유머감각이 뛰어난 코미디언입니다. 모든 대답에 재미있는 농담을 섞어주세요."},
            #{"role": "system", "content": "너는 중학생 국어 AI 튜터야. 학생들이 국어에 대한 질문에는 자세하고 친절하게 대답해. 그런데, 국어 학습 이외의 내용을 질문하면 "너 벌점 10점!!"이라고 말해줘."},
            {"role": "system", "content": "당신은 최고급 호텔의 완벽한 집사입니다. 항상 정중하고 격식있게 말하세요."},
            {"role": "user", "content": "1+1은?"}
            #{"role": "user", "content": "나는 국어 학습을 열심히 하고 싶은데, 배가 고파서 잘 안되네. 오늘 점심은 떡볶이가 좋을까 자장면이 좋을까??"}
        ]
    )
    print("5살 응답:", response2.choices[0].message.content)

test_roles()