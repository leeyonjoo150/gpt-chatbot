#openai api 실습 환경 구성 확인
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print("API_KEY : ", api_key)