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
        loadContent('/show/emotion');
        // window.location.href = '/show/emotion';
    }
});

// 페이드 아웃 및 새 콘텐츠 로드 함수
function loadContent(url) {
    // 동적 페이지 구현
    const dynamicContent = document.getElementById('dynamicContent');

    // 페이드 아웃
    dynamicContent.classList.add('hidden');

    // CSS 트랜지션을 기다린 후 페이지에 따른
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

                            // Summary 내용 표시
                            if (data && data.summary) {
                                descriptionElement.innerHTML = data.summary;
                            }

                            // Keywords 및 신뢰도 표시
                            if (data && data.keywords) {
                                const labels = data.keywords.map(keyword => keyword.text.content);
                                const confidences = data.keywords.map(keyword => {
                                    // certaintyAssessment 객체와 confidence 속성이 있는지 확인
                                    if (keyword.certaintyAssessment && typeof keyword.certaintyAssessment.confidence === 'number') {
                                        return keyword.certaintyAssessment.confidence.toFixed(3);
                                    } else {
                                        // certaintyAssessment 객체 또는 confidence 속성이 없는 경우 안전한 기본값 반환
                                        return '0.000';
                                    }
                                });

                                createKeywordsChart(labels, confidences);
                            }
                        })
                        .catch(error => {
                            console.error('Error fetching voice text data:', error);
                        });
                }

                // '/show/emotion' 페이지가 로드된 후 추가적인 JSON 데이터 요청
                if (url === '/show/emotion') {
                    fetch('/get/emotion')
                        .then(response => response.json())
                        .then(data => {

                                createEmotionChart(data);
                                showEmotionTable(data);
                                showEmotionImage(data);

                        })
                        .catch(error => {
                            console.error('Error fetching voice text data:', error);
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

// 보이스 파일 드래그 앤 드롭
function setupFileDragAndDrop() {
    const dropArea = document.getElementById('dropArea');
    const fileInput = document.getElementById('fileInput');
    const fileInputLink = document.getElementById('fileInputLink');

    // 파일 입력 필드 열기
    fileInputLink.addEventListener('click', (e) => {
        e.preventDefault();
        fileInput.click();
    });

    fileInput.addEventListener('change', function(e) {
        handleFiles(this.files);
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
        document.getElementById('downloadFiles').style.display = 'none';

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
                        document.getElementById('downloadFiles').style.display = 'flex';
                        completeMessage.style.display = 'none';
                    }, 3000);
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
                    beginAtZero: true,
                }
            }
        }
    });
}

// emotion 차트 만들기
function createEmotionChart(patient) {
    const chartTitle = "The patient's sentiment analysis chart";
    var sentences = patient.text_contents;
    var sentiScores = patient.senti_scores;
    var sentiMagnitudes = patient.senti_magnitudes;
    var overallScore = patient.doc_sentiment_score;
    var overallMagnitude = patient.doc_sentiment_magnitude;

    // 긍정, 부정 기준선을 그래프에 그리기 위해 리스트에 문장 개수만큼 채워 넣음
    var positiveBaseline = new Array(sentiScores.length).fill(0.25);
    var negativeBaseline = new Array(sentiScores.length).fill(-0.25);

    // labels를 sentence 개수만큼 만듦 => text1, text2, ...
    var labels = []
    for (var i = 1; i <= sentences.length; i++) {
        labels.push("");
    }

    // 차트 구성 설정
    const data = {
        labels: labels,
        datasets: [{
            label: 'Sentiment Scores',
            backgroundColor: 'rgb(000, 153, 255)',
            borderColor: 'rgb(000, 153, 255)',
            data: sentiScores,
        },
            {
                label: 'Sentiment Magnitudes',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: sentiMagnitudes,
            },
            {
                label: 'Positive Baseline',
                backgroundColor: 'rgb(102, 102, 102)',
                borderColor: 'rgb(102, 102, 102)',
                borderDash: [5, 5],
                data: positiveBaseline,
            },
            {
                label: 'Negative Baseline',
                backgroundColor: 'rgb(102, 102, 102)',
                borderColor: 'rgb(102, 102, 102)',
                borderDash: [5, 5],
                data: negativeBaseline,
            }]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false, // 이 부분을 추가
            scales: {
                x:{
                    ticks:{
                        font:{
                            size: 14
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: {
                            size: 14 // 범례 글씨 크기 수정
                        }
                    }
                },
                title: {
                    display: true,
                    text: chartTitle,
                    font: {
                        size: 16 // 제목 글씨 크기 수정
                    }
                }
            }
        },
    };

    const myChart = new Chart(
        document.getElementById('patientChart'),
        config
    );
}

// 감정분석 테이블 삽입
function showEmotionTable(patient){
    var sentences = patient.text_contents;
    var sentiScores = patient.senti_scores;
    var sentiMagnitudes = patient.senti_magnitudes;
    var overallScore = patient.doc_sentiment_score;
    var overallMagnitude = patient.doc_sentiment_magnitude;

    for (var i = 0; i < sentiScores.length; i++) {
        if (sentiScores[i] < -0.25 || sentiScores[i] > 0.25) {
            var row = document.createElement('tr');
            var cell1 = document.createElement('td');
            var cell2 = document.createElement('td');
            var cell3 = document.createElement('td');

            cell1.textContent = sentences[i];
            cell2.textContent = sentiScores[i];
            cell3.textContent = sentiMagnitudes[i];

            if (sentiScores[i] >= 0.25 && sentiScores[i] <= 1) {
                cell2.classList.add('positive');
                cell3.classList.add('positive');
            } else if (sentiScores[i] >= -1 && sentiScores[i] < -0.25) {
                cell2.classList.add('negative');
                cell3.classList.add('negative');
            }

            row.appendChild(cell1);
            row.appendChild(cell2);
            row.appendChild(cell3);
            document.querySelector('.chart__table table').appendChild(row);
        }
    }
}

// 오늘의 기분 그림
function showEmotionImage(patient){
    const sentimentScore = patient.doc_sentiment_score;

    const sadImage = document.getElementById('sadImage');
    const noCommentImage = document.getElementById('noCommentImage');
    const happyImage = document.getElementById('happyImage');

    if (sentimentScore > 0.25) {
        sadImage.src = '/static/images/sad_disabled.png';
        noCommentImage.src = '/static/images/nocomment_disabled.png';
        happyImage.src = '/static/images/happy.png';
    } else if (sentimentScore < -0.25) {
        sadImage.src = '/static/images/sad.png';
        noCommentImage.src = '/static/images/nocomment_disabled.png';
        happyImage.src = '/static/images/happy_disabled.png';
    } else {
        sadImage.src = '/static/images/sad_disabled.png';
        noCommentImage.src = '/static/images/nocomment.png';
        happyImage.src = '/static/images/happy_disabled.png';
    }
}
