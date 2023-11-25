
// 동적 페이지, SPA 구현

// 첫 페이지 로드
document.addEventListener('DOMContentLoaded', (event) => {
    loadContent('/main');
});

// 버튼별 페이지 이동
document.getElementById('dynamicContent').addEventListener('click', function (event) {
    if (event.target.id === 'viewTextSummary') {
        event.preventDefault();
        loadContent('/show/voicetext');
    }
    if (event.target.id === 'startEmotionAnalysis') {
        event.preventDefault();
        // loadContent('/show/emotion');
        window.location.href = '/show/emotion';
    }
});

// 페이드 아웃 및 새 콘텐츠 로드 함수
function loadContent(url) {
    const dynamicContent = document.getElementById('dynamicContent');
    // 페이드 아웃
    dynamicContent.classList.add('hidden');

    // CSS 트랜지션을 기다립니다
    setTimeout(() => {
        fetch(url)
            .then(response => response.text())
            .then(html => {
                // 콘텐츠 업데이트 및 페이드 인
                dynamicContent.innerHTML = html;
                dynamicContent.classList.remove('hidden');

                // '/show/voicetext' 페이지가 로드된 후 추가적인 JSON 데이터 요청
                if (url === '/show/voicetext') {
                    fetch('/get/voicetext')
                        .then(response => response.json())
                        .then(data => {
                            const descriptionElement = document.querySelector('.overlay_summary_description');
                            const keywordsElement = document.querySelector('.overlay-summary-right');

                            // Summary 내용 표시
                            if (data && data.summary) {
                                descriptionElement.innerHTML = data.summary;
                            }

                            // Keywords 및 신뢰도 표시
                            if (data && data.keywords) {
                                data.keywords.forEach(keyword => {
                                    const labels = data.keywords.map(keyword => keyword.text.content);
                                    const confidences = data.keywords.map(keyword => keyword.certaintyAssessment.confidence.toFixed(3));

                                    createKeywordsChart(labels, confidences);
                                });
                            }
                        });
                }

                setupArrowClickListener();

                // 필요한 경우 추가 초기화 함수 호출
                if (url === '/main') {
                    setupFileDragAndDrop();
                }
            });
    }, 300); // CSS 트랜지션 시간과 일치
}

// 화살표 클릭 이벤트 리스너 설정 함수
function setupArrowClickListener() {
    const arrowContainer = document.querySelector('.arrow-container');
    if (arrowContainer) {
        arrowContainer.addEventListener('click', function (event) {
            // Arrow 부분이 클릭되면 main_page 로드
            if (event.target.closest('.arrow')) {
                event.preventDefault();
                loadContent('/main');
            }
        });
    }
}

// 보이스 넣는 설정
function setupFileDragAndDrop() {
    const dropArea = document.getElementById('dropArea');
    const fileInput = document.getElementById('fileInput');
    const fileInputLink = document.getElementById('fileInputLink');

    // 파일 입력 필드 열기
    fileInputLink.addEventListener('click', (e) => {
        e.preventDefault();
        fileInput.click();
    });

    // 드래그 이벤트 방지
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    // 드래그 활성화/비활성화 스타일
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        dropArea.classList.add('active');
    }

    function unhighlight(e) {
        dropArea.classList.remove('active');
    }

    // 파일 드롭 처리
    dropArea.addEventListener('drop', handleDrop, false);
    let isFileUploaded = false;

    function handleDrop(e) {
        if (isFileUploaded) {
            return; // 파일이 이미 업로드된 경우, 추가 처리 방지
        }
        let dt = e.dataTransfer;
        let files = dt.files;

        handleFiles(files);
    }

    function handleFiles(files) {
        ([...files]).forEach(uploadFile);
    }

    function uploadFile(file) {
        let formData = new FormData();
        formData.append('file', file); // 'file'은 서버에서 받을 때 사용할 키
        // 업로드 애니메이션 및 메시지 표시
        dropArea.classList.add('uploading')
        document.getElementById('loadingSpinner').style.display = 'block';
        document.getElementById('dropAreaMessage').style.display = 'none';

        // 파일 업로드 요청
        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                // 업로드 완료시 스피너 숨기기
                document.getElementById('loadingSpinner').style.display = 'none';

                if (data.message === 'File uploaded successfully!') {
                    dropArea.classList.remove('uploading');
                    dropArea.classList.add('uploaded');

                    // 업로드 완료 메시지 표시
                    const completeMessage = document.getElementById('completeMessage');
                    completeMessage.style.display = 'block';

                    // 3초 후에 'uploaded' 클래스 제거 + 원래대로 돌리기
                    setTimeout(() => {
                        dropArea.classList.remove('uploaded');
                        document.getElementById('dropAreaMessage').style.display = 'block';
                        completeMessage.style.display = 'none';
                    }, 3000);
                    // 업로드 완료시 쿠키에 파일 이름 저장
                    document.cookie = "uploadedFileName=" + encodeURIComponent(data.filename) + "; path=/";
                } else {
                    document.getElementById('dropAreaMessage').innerText = "Upload failed";
                }
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('dropAreaMessage').innerText = "Upload failed";
            });
    }
}

// keyword 차트 만들기
function createKeywordsChart(labels, confidences) {
    const ctx = document.getElementById('summaryChart').getContext('2d');
    const keywordsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Confidence Scores',
                data: confidences,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}


