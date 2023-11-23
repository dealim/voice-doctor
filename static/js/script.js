
// 동적 페이지, SPA 구현

// 첫 페이지 로드
document.addEventListener('DOMContentLoaded', (event) => {
    loadContent('/main');
});

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

                            descriptionElement.innerHTML += `
                                Name: ${data.name}
                                Age: ${data.age}
                            `;
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

        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.message === 'File uploaded successfully!') {
                    console.log(data);
                    isFileUploaded = true; // 업로드 상태 업데이트
                    document.getElementById('dropAreaMessage').innerText = "업로드가 완료 되었습니다"; // 메시지 변경
                    dropArea.classList.add('uploaded'); // 업로드된 상태 스타일 적용
                } else {
                    document.getElementById('dropAreaMessage').innerText = "업로드 실패";
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
}



