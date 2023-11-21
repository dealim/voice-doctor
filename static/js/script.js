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
        if(data.message === 'File uploaded successfully!') {
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

