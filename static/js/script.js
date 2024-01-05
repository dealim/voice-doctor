// 첫 페이지 로드
$(() => {
    loadContent('/main');
})

// 버튼별 페이지 이동
$(()=>{
    $('#dynamicContent').on('click', function (e) {
        var target = $(e.target);

        if (target.is('#viewTextSummary')) {
            e.preventDefault();
            loadContent('/show/summary');
        }
        if (target.is('#viewEmotionAnalysis')) {
            e.preventDefault();
            loadContent('/show/emotion');
        }
        if (target.is('#viewOcrAnalysis')) {
            e.preventDefault();
            loadContent('/show/ocr');
        }
        if(target.is('#viewStt')) {
            e.preventDefault();
            loadContent('/show/stt');
        }
    });
});

// 토글
$(document).on('click', '#switch', (e) => {
    const switchBtn = document.getElementById("switch");
    let currentState = switchBtn.getAttribute('data-state');
    const icon = document.getElementById("voice-recording-icon");
    const dropAreaMessage = document.getElementById("dropAreaMessage");
    const emotionBtn = document.getElementById("viewEmotionAnalysis");
    const summaryBtn = document.getElementById("viewTextSummary");
    const ocrBtn = document.getElementById("viewOcrAnalysis");

    if (currentState === 'voice') {
        switchBtn.setAttribute('data-state', 'pdf');
        icon.addEventListener('click', preventClickEvent);
        icon.src = "static/images/pdf.svg";
        icon.alt = "pdf";
        dropAreaMessage.innerHTML = 'drag and drop pdf file here <a href="#" id="fileInputLink">browse for files</a>';
        emotionBtn.style.display = "none";
        summaryBtn.style.display = "none";
        ocrBtn.style.display = "flex";
        icon.addEventListener('click', fileInputClick);
        setupFileDragAndDrop();
    } else {
        switchBtn.setAttribute('data-state', 'voice');
        icon.removeEventListener('click', preventClickEvent);
        icon.src = "static/images/recording.svg";
        icon.alt = "recording";
        dropAreaMessage.innerHTML = 'click icon to record voice or drag and drop file <a href="#" id="fileInputLink">browse for files</a>';
        emotionBtn.style.display = "flex";
        summaryBtn.style.display = "flex";
        ocrBtn.style.display = "none";
        icon.removeEventListener('click', fileInputClick);
        setupFileDragAndDrop();
    }

});

// 파일 다운로드 이벤트(동적 페이지에 이벤트 구현)
document.body.addEventListener('click', function (e) {
    if (e.target.matches('.downloadFiles a')) {
        e.preventDefault();

        // 클릭된 링크에서 URL과 파일 이름 추출
        const fileUrl = e.target.href;
        const fileName = e.target.getAttribute('download');

        // 파일 다운로드를 위한 fetch 요청
        fetch(fileUrl)
            .then(response => response.blob()) // Blob 형태로 응답을 받음
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = fileName; // 다운로드할 파일 이름 설정
                document.body.appendChild(a);
                a.click(); // 링크 클릭 이벤트 트리거
                window.URL.revokeObjectURL(url); // URL 메모리 해제
            })
            .catch(() => console.error('Could not download the file.'));
    }
});


// 페이드 아웃 및 새 콘텐츠 로드 함수
function loadContent(url) {
    const dynamicContent = document.getElementById('dynamicContent');

    // 페이드 아웃
    dynamicContent.classList.add('hidden');

    // CSS 트랜지션을 기다린 후 페이지 띄우기
    setTimeout(() => {
        fetch(url)
            .then(response => response.text())
            .then(html => {

                // 콘텐츠 업데이트 및 페이드 인
                dynamicContent.innerHTML = html;
                dynamicContent.classList.remove('hidden');

                // '/show/summary' 페이지가 로드된 후 추가적인 JSON 데이터 요청
                if (url === '/show/summary') {
                    fetch('/get/summary')
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

                if (url === '/show/ocr') {
                    fetch('/get/ocr')
                        .then(response => response.json())
                        .then(data => {

                            showOCR(data);

                        })
                }

                if (url === '/show/stt') {
                    fetch('/get/stt')
                        .then(response => response.json())
                        .then(data => {
                            const descriptionElement = document.querySelector('.overlay_summary_description');
                            console.log(data);
                            if (data && data[0].transcript) {
                                descriptionElement.innerHTML = data[0].transcript;
                            }
                        })
                }

                // 드래그앤드랍 기능 셋업
                if (url === '/main') {
                    setupFileDragAndDrop();
                }

                setupArrowClickListener(url);
            });
    }, 300); // CSS 트랜지션 시간과 일치
}

// 화살표 클릭 이벤트 리스너 설정 함수
function setupArrowClickListener(url) {
    const arrowContainer = document.querySelector('.arrow-container');
    if (arrowContainer) {
        arrowContainer.addEventListener('click', function (e) {

            if (e.target.closest('.arrow')) {
                e.preventDefault();
                console.log(url);
                if(url === '/show/stt'){
                    loadContent('/show/summary');
                }else{
                    loadContent('/main');
                }
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

    fileInput.addEventListener('change', function (e) {
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

    // 토글 설정
    document.querySelector('.toggle').addEventListener('click', toggle);
}

// 파일 업로드 하기
function uploadFile(file) {
    let formData = new FormData();
    formData.append('file', file); // 'file'은 서버에서 받을 때 사용할 키

    // 업로드 애니메이션 및 메시지 표시
    dropArea.classList.add('uploading');
    document.getElementById('loadingSpinner').style.display = 'block';
    document.getElementById('dropAreaMessage').style.display = 'none';
    document.getElementById('voice-recording-icon').style.display = 'none';

    // 파일 업로드 요청
    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(json => Promise.reject(new Error(json.error || 'Unknown server error')));
            }
            return response.json();
        })
        .then(data => {
            if (data.message === 'File uploaded successfully!') {
                // 업로드 완료시 스피너 숨기기
                document.getElementById('loadingSpinner').style.display = 'none';
                dropArea.classList.remove('uploading');
                dropArea.classList.add('uploaded');

                // 업로드 완료 메시지 표시
                const completeMessage = document.getElementById('completeMessage');
                completeMessage.style.display = 'block';

                // 3초 후에 'uploaded' 클래스 제거 + 원래대로 돌리기
                setTimeout(() => {
                    dropArea.classList.remove('uploaded');
                    document.getElementById('dropAreaMessage').style.display = 'block';
                    document.getElementById('voice-recording-icon').style.display = 'block';
                    completeMessage.style.display = 'none';
                }, 3000);
            }
        })
        .catch(error => {
            console.error('Error:', error.message);
            document.getElementById('loadingSpinner').style.display = 'none';
            document.getElementById('failedMessage').style.display = 'block';
            dropArea.classList.remove('uploading');
            dropArea.classList.add('failed');

            setTimeout(() => {
                dropArea.classList.remove('failed');
                document.getElementById('failedMessage').style.display = 'none';
                document.getElementById('dropAreaMessage').style.display = 'block';
                document.getElementById('voice-recording-icon').style.display = 'block';
            }, 3000);

        });
}

// 녹음기 아이콘에 녹음 기능
let audioStream;
let recorder;
let isRecording = false;
$(document.body).click(function (e){
    // 클릭된 요소가 voice-recording-icon인지 확인
    if (e.target.matches('#voice-recording-icon')) {
        // 녹음 상태 확인 후 시작 또는 중지
        if (isRecording) {
            stopRecording();
        } else {
            startRecording();
        }
    }
});

// 사용자의 오디오 스트림을 얻는 함수
function startRecording() {
    let audioType = 'audio/wav';

    navigator.mediaDevices.getUserMedia({audio: true})
        .then(stream => {
            audioStream = stream;
            // RecordRTC 설정
            recorder = new RecordRTC(audioStream, {
                type: 'audio',
                mimeType: audioType,
                recorderType: RecordRTC.StereoAudioRecorder, // StereoAudioRecorder 사용
                sampleRate: 44100,
                desiredSampRate: 44100, // 원하는 샘플레이트 설정
                numberOfAudioChannels: 1 // 모노 채널 설정
            });

            // 펄스 애니메이션 클래스 추가
            document.getElementById("voice-recording-icon").src = "static/images/recording-red.svg";
            document.getElementById("voice-recording-icon").classList.add("pulse-animation");

            recorder.startRecording();

            isRecording = true;
        }).catch(error => {
        console.error("오디오 녹음을 시작할 수 없습니다.", error);
    });
}

// 녹음 중지 함수
function stopRecording() {
    recorder.stopRecording(() => {
        let audioBlob = recorder.getBlob();

        // 오디오 처리 및 업로드 로직
        uploadAudio(audioBlob, 'wav');

        // 오디오 파일 분석 시작
        uploadFile(audioBlob, 'wav');

        // 미디어 스트림 트랙 종료
        audioStream.getAudioTracks().forEach(track => track.stop());

        // UI 업데이트 (예: 녹음 중지 상태 표시)
        document.getElementById("voice-recording-icon").classList.remove("pulse-animation");
        document.getElementById("voice-recording-icon").src = "static/images/recording.svg";
        isRecording = false;

    });
}

// 녹음 파일(blob)을 서버로 전송하기
function uploadAudio(blob, extName) {
    const formData = new FormData();
    formData.append('audio', blob, "recording." + extName);

    fetch('/api/record', { // Flask 서버의 엔드포인트
        method: 'POST',
        body: formData
    })
        .then(response => response.text())
        .then(data => {
            console.log('Upload success:', data);
        })
        .catch(error => {
            console.error('Upload failed:', error);
        });
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

// emotion 차트
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
            scales: {
                x: {
                    ticks: {
                        font: {
                            size: 14
                        }
                    }
                },
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

    function updateChartOptions() {
        var width = window.innerWidth;
        // 화면 크기에 따라 차트 옵션을 조정
        if (width < 600) {
            myChart.options.plugins.legend.labels.font.size = 8;
            myChart.options.plugins.legend.display = false;
        } else {
            myChart.options.plugins.legend.labels.font.size = 14;
            myChart.options.plugins.legend.position = 'top';
        }
        myChart.update(); // 차트 업데이트
    };

    window.addEventListener('resize', updateChartOptions);
}

// 감정분석 테이블 삽입
function showEmotionTable(patient) {
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
            document.querySelector('.emotion-table table').appendChild(row);
        }
    }
}

// 오늘의 기분 그림
function showEmotionImage(patient) {
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

// ocr 파싱
function showOCR(data) {
    const summaryLeft1 = document.getElementById('overlay_summary_description1');
    const summaryLeft2 = document.getElementById('overlay_summary_description2');
    const summaryRight = document.querySelector('.overlay-summary-right .patient-details');
    if(isJapaneseData(data)){
        summaryLeft1.innerHTML = `
                <strong>名前 :</strong> ${data["名前"]}<br>
                <strong>診療日 :</strong> ${data["診療日"]}<br>
                <strong>性別 :</strong> ${data["性別"]}<br>
                <strong>生年月日 :</strong> ${data["生年月日"]}<br>
            `;

        summaryLeft2.innerHTML = `
                <strong>医師 :</strong> ${data["医師"]}<br>
                <strong>患者 :</strong> ${data["患者"]}<br>
                <strong>主訴 :</strong> ${data["主訴"]}<br>
            `;

        // 우측 상세 정보 구성
        summaryRight.innerHTML = `
                <strong>症状の発生時期 :</strong> ${data["症状の発生時期"]}<br>
                <strong>けがの原因 :</strong> ${data["けがの原因"]}<br>
                <strong>何が痛みを和らげますか? :</strong> ${data["何が痛みを和らげますか?"]}<br>
                <strong>何が痛みを悪化させますか? :</strong> ${data["何が痛みを悪化させますか?"]}
            `;


    } else {
        // 좌측 요약 정보 구성
        summaryLeft1.innerHTML = `
                <strong>Name :</strong> ${data["NAME"]}<br>
                <strong>Date of Service :</strong> ${data["DATE OF SERVICE"]}<br>
                <strong>Doctor :</strong> ${data["DOCTOR"]}<br>
            `;

        summaryLeft2.innerHTML = `
                <strong>Chief Complaint :</strong> ${data["CHIEF COMPLAINT"]}<br>
                <strong>Date of Birth :</strong> ${data["DATE OF BIRTH"]}<br>
                <strong>Patient :</strong> ${data["PATIENT"]}<br>
            `;

        // 우측 상세 정보 구성
        summaryRight.innerHTML = `
                <strong>Onset of Symptoms :</strong> ${data["ONSET OF SYMPTOMS"]}<br>
                <strong>Mechanism of Injury :</strong> ${data["MECHANISM OF INJURY"]}<br>
                <strong>What makes the pain better? :</strong> ${data["What makes the pain better?"]}<br>
                <strong>What makes the pain worse? :</strong> ${data["What makes the pain worse?"]}
            `;

    }
}

function isJapaneseData(data) {
    return data.hasOwnProperty("名前") || data.hasOwnProperty("診療日") || data.hasOwnProperty("生年月日");
}

// 클릭 이벤트 막는 함수
function preventClickEvent(e) {
    e.preventDefault();
    e.stopPropagation();
}

// pdf 아이콘 기능 설정
function fileInputClick(e) {
    const fileInput = document.getElementById('fileInput');
    e.preventDefault();
    fileInput.click();
}

// 토글 함수
function toggle() {
    let btn = this;
    btn.classList.add('animation');
    btn.classList.toggle('active');
    let newElem = btn.cloneNode(true);
    btn.parentNode.replaceChild(newElem, btn);
    newElem.addEventListener('click', toggle);
}