from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from openai import OpenAI
from django.conf import settings
import json
import logging

from .models import Conversation, Message

logger = logging.getLogger(__name__)

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=settings.OPENAI_API_KEY)


def index(request):
    """메인 페이지"""
    if request.user.is_authenticated:
        return redirect('chat:chat')
    return redirect('chat:login')


def login_view(request):
    """로그인 페이지"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat:chat')
        else:
            messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')

    return render(request, 'chat/login.html')


def register_view(request):
    """회원가입 페이지"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password != password_confirm:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return render(request, 'chat/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, '이미 존재하는 아이디입니다.')
            return render(request, 'chat/register.html')

        user = User.objects.create_user(username=username, password=password)
        messages.success(request, '회원가입이 완료되었습니다. 로그인해주세요.')
        return redirect('chat:login')

    return render(request, 'chat/register.html')


def logout_view(request):
    """로그아웃"""
    logout(request)
    return redirect('chat:login')


@login_required
def chat_view(request, conversation_id=None):
    """채팅 페이지"""
    conversation = None
    messages = []

    if conversation_id:
        conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
        messages = conversation.messages.filter(is_active=True)

    # 사용자의 대화 목록 가져오기
    conversations = Conversation.objects.filter(user=request.user, is_active=True)

    context = {
        'conversation': conversation,
        'messages': messages,
        'conversations': conversations,
    }

    return render(request, 'chat/chat.html', context)


@login_required
def new_chat(request):
    """새 대화 시작"""
    conversation = Conversation.objects.create(
        user=request.user,
        title='새 대화'
    )
    return redirect('chat:chat_detail', conversation_id=conversation.id)


@csrf_exempt
@login_required
def send_message(request):
    """메시지 전송 및 AI 응답 처리"""
    if request.method != 'POST':
        return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)

    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id')

        if not user_message:
            return JsonResponse({'error': '메시지가 비어있습니다.'}, status=400)

        # 대화 가져오기 또는 생성
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
        else:
            conversation = Conversation.objects.create(
                user=request.user,
                title=user_message[:50] + '...' if len(user_message) > 50 else user_message
            )

        # 사용자 메시지 저장
        user_msg = Message.objects.create(
            conversation=conversation,
            role='user',
            content=user_message
        )

        # OpenAI API 호출
        try:
            # 대화 히스토리 가져오기
            messages_for_api = conversation.get_messages_for_api()

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages_for_api
            )

            ai_response = response.choices[0].message.content

            # AI 응답 저장
            ai_msg = Message.objects.create(
                conversation=conversation,
                role='assistant',
                content=ai_response
            )

            # 대화 업데이트 시간 갱신
            conversation.save()

            return JsonResponse({
                'success': True,
                'conversation_id': conversation.id,
                'user_message': user_message,
                'ai_response': ai_response,
                'message_id': ai_msg.id
            })

        except Exception as e:
            logger.error(f"OpenAI API 오류: {str(e)}")
            return JsonResponse({'error': f'AI 응답 생성 중 오류가 발생했습니다: {str(e)}'}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({'error': '잘못된 JSON 형식입니다.'}, status=400)
    except Exception as e:
        logger.error(f"메시지 전송 오류: {str(e)}")
        return JsonResponse({'error': '메시지 전송 중 오류가 발생했습니다.'}, status=500)


@login_required
def get_conversations(request):
    """사용자의 대화 목록 반환"""
    conversations = Conversation.objects.filter(user=request.user, is_active=True)
    data = []
    for conv in conversations:
        data.append({
            'id': conv.id,
            'title': conv.title,
            'updated_at': conv.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return JsonResponse({'conversations': data})