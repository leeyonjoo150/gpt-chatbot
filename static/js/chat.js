// 채팅 관련 JavaScript

let isLoading = false;

$(document).ready(function() {
    initializeChat();
});

function initializeChat() {
    // 메시지 전송 폼 이벤트
    $('#message-form').on('submit', function(e) {
        e.preventDefault();
        sendMessage();
    });

    // Enter 키 이벤트
    $('#message-input').on('keydown', function(e) {
        handleEnterKey(e, sendMessage);
    });

    // 대화 목록 클릭 이벤트
    $('.conversation-item').on('click', function() {
        const conversationId = $(this).data('conversation-id');
        window.location.href = `/chat/${conversationId}/`;
    });

    // 페이지 로드 시 스크롤을 맨 아래로
    scrollToBottom(document.getElementById('messages-container'));

    // 텍스트 영역 자동 높이 조절
    autoResizeTextarea('#message-input');
}

function sendMessage() {
    if (isLoading) return;

    const messageInput = $('#message-input');
    const message = messageInput.val().trim();

    if (!message) {
        messageInput.focus();
        return;
    }

    // UI에 사용자 메시지 즉시 추가
    addMessageToUI(message, 'user');

    // 입력창 비우기
    messageInput.val('').css('height', 'auto');

    // 로딩 상태 설정
    isLoading = true;
    showTypingIndicator();

    // AJAX 요청
    $.ajax({
        url: '/send-message/',
        type: 'POST',
        headers: {
            'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()
        },
        data: JSON.stringify({
            message: message,
            conversation_id: currentConversationId
        }),
        contentType: 'application/json',
        success: function(response) {
            if (response.success) {
                // 타이핑 인디케이터 제거
                hideTypingIndicator();

                // AI 응답 추가
                addMessageToUI(response.ai_response, 'assistant');

                // 현재 대화 ID 업데이트
                if (!currentConversationId) {
                    currentConversationId = response.conversation_id;
                    // URL 업데이트 (새 대화인 경우)
                    window.history.pushState({}, '', `/chat/${response.conversation_id}/`);
                    // 사이드바 새로고침
                    updateConversationList();
                }
            } else {
                showAlert('메시지 전송에 실패했습니다.', 'danger');
                hideTypingIndicator();
            }
        },
        error: function(xhr) {
            let errorMessage = '메시지 전송 중 오류가 발생했습니다.';
            if (xhr.responseJSON && xhr.responseJSON.error) {
                errorMessage = xhr.responseJSON.error;
            }
            showAlert(errorMessage, 'danger');
            hideTypingIndicator();
        },
        complete: function() {
            isLoading = false;
            messageInput.focus();
        }
    });
}

function addMessageToUI(content, role) {
    const messagesContainer = $('#messages');
    const currentTime = new Date().toLocaleTimeString('ko-KR', {
        hour: '2-digit',
        minute: '2-digit'
    });

    let messageHtml = '';

    if (role === 'user') {
        messageHtml = `
            <div class="message-wrapper mb-3">
                <div class="d-flex justify-content-end">
                    <div class="message user-message bg-primary text-white p-3 rounded-3" style="max-width: 80%;">
                        <div class="message-content">${content.replace(/\n/g, '<br>')}</div>
                        <small class="message-time text-light opacity-75">
                            ${currentTime}
                        </small>
                    </div>
                </div>
            </div>
        `;
    } else {
        messageHtml = `
            <div class="message-wrapper mb-3">
                <div class="d-flex justify-content-start">
                    <div class="message ai-message bg-dark text-white p-3 rounded-3" style="max-width: 80%;">
                        <div class="d-flex align-items-center mb-2">
                            <i class="fas fa-robot text-info me-2"></i>
                            <strong>AI Assistant</strong>
                        </div>
                        <div class="message-content">${content.replace(/\n/g, '<br>')}</div>
                        <small class="message-time text-light opacity-75">
                            ${currentTime}
                        </small>
                    </div>
                </div>
            </div>
        `;
    }

    messagesContainer.append(messageHtml);
    scrollToBottom(document.getElementById('messages-container'));

    // 환영 메시지가 있다면 제거
    $('.text-center.text-muted').parent().remove();
}

function showTypingIndicator() {
    const typingHtml = `
        <div class="message-wrapper mb-3" id="typing-indicator">
            <div class="d-flex justify-content-start">
                <div class="message ai-message bg-dark text-white p-3 rounded-3">
                    <div class="d-flex align-items-center mb-2">
                        <i class="fas fa-robot text-info me-2"></i>
                        <strong>AI Assistant</strong>
                    </div>
                    <div class="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            </div>
        </div>
    `;

    $('#messages').append(typingHtml);
    scrollToBottom(document.getElementById('messages-container'));
}

function hideTypingIndicator() {
    $('#typing-indicator').remove();
}

function updateConversationList() {
    // 대화 목록 새로고침
    $.ajax({
        url: '/get-conversations/',
        type: 'GET',
        success: function(response) {
            const conversationList = $('#conversation-list');
            conversationList.empty();

            response.conversations.forEach(function(conv) {
                const isActive = currentConversationId == conv.id ? 'bg-primary' : 'bg-dark';
                const date = new Date(conv.updated_at).toLocaleDateString('ko-KR', {
                    month: 'numeric',
                    day: 'numeric'
                });

                const convHtml = `
                    <div class="conversation-item mb-2 p-2 rounded ${isActive}"
                         data-conversation-id="${conv.id}"
                         style="cursor: pointer;">
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="text-truncate flex-grow-1" title="${conv.title}">
                                ${conv.title.substring(0, 30)}${conv.title.length > 30 ? '...' : ''}
                            </div>
                            <small class="text-muted ms-2">
                                ${date}
                            </small>
                        </div>
                    </div>
                `;

                conversationList.append(convHtml);
            });

            // 클릭 이벤트 다시 바인딩
            $('.conversation-item').on('click', function() {
                const conversationId = $(this).data('conversation-id');
                window.location.href = `/chat/${conversationId}/`;
            });
        }
    });
}

function autoResizeTextarea(selector) {
    $(selector).on('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });
}

function showAlert(message, type = 'info') {
    // 간단한 alert 구현 (Bootstrap toast 또는 다른 방식으로 개선 가능)
    alert(message);
}

function scrollToBottom(element) {
    element.scrollTop = element.scrollHeight;
}

function handleEnterKey(e, callback) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        callback();
    }
}