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

function handleDrop(e) {
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

    fetch('/upload', { // Flask 엔드포인트
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
