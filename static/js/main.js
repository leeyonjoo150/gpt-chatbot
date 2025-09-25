// 기본 JavaScript 함수들

// 페이지 로드 시 실행
$(document).ready(function() {
    // 자동 높이 조절 텍스트 영역
    autoResizeTextarea();

    // 모바일 반응형 처리
    handleMobileResponsive();
});

// 텍스트 영역 자동 높이 조절
function autoResizeTextarea() {
    $('textarea').on('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
}

// 모바일 반응형 처리
function handleMobileResponsive() {
    if (window.innerWidth <= 768) {
        // 모바일에서 사이드바 토글 버튼 추가 (필요시)
        // 추후 구현 가능
    }
}

// 스크롤을 맨 아래로
function scrollToBottom(element) {
    element.scrollTop = element.scrollHeight;
}

// 메시지 시간 포맷팅
function formatTime(date) {
    return new Date(date).toLocaleTimeString('ko-KR', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// 알림 메시지 표시
function showAlert(message, type = 'info') {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    // 기존 알림 제거
    $('.alert').remove();

    // 새 알림 추가
    $('body').prepend(alertHtml);

    // 5초 후 자동 제거
    setTimeout(() => {
        $('.alert').fadeOut();
    }, 5000);
}

// 로딩 상태 표시/숨김
function showLoading() {
    $('#loading-modal').modal('show');
}

function hideLoading() {
    $('#loading-modal').modal('hide');
}

// Enter 키 처리
function handleEnterKey(event, callback) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        callback();
    }
}