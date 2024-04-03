# VoiceDoctor 🧑🏼‍⚕️

환자가 녹음한 문진 내용을 입력해 감정분석, 요약, 키워드 분석 결과를 보여주는 CDSS.  
(CDSS : 환자로부터 얻어진 임상 정보를 바탕으로 의료인이 질병을 진단하고 치료할 때 의사결정을 도와주는 시스템) 
> [!Important]
> Google Cloud API를 활용하였기 떄문에 사전에 미리 구글 서비스키를 받아두어야 합니다.
> 공식 문서를 따라 서비스키 `json` 파일을 받아 두시기 바랍니다.
> - [Google Cloud Natural Language (감정 분석)](https://cloud.google.com/natural-language/docs)
> - [Google Cloud Healthcare API](https://cloud.google.com/healthcare/docs)
> - [Google Cloud Vision API (OCR)](https://cloud.google.com/vision/docs/ocr)
> - [Google Cloud Text-to-Speech](https://cloud.google.com/text-to-speech/docs)
> - [Vertex AI](https://cloud.google.com/vertex-ai/docs) 


## Features

- Speech To Text
  - 환자/의사 대화 실시간 녹음
  - 텍스트 감정분석
  - 다중 언어 지원 : 한, 영, 일
  - wav, flac 파일 지원
- PDF
    - OCR을 통한 문진표 디지털화
- Vertex Ai
    - 의사-환자 대화 요약
    - 의심 질환 예측
    - 환자에 대한 추가 질문 생성

## System Requirements

- Mac OS: macOS 10.9 (Mavericks) 이상
- Linux: 커널 버전 3.10 이상을 권장(Ubuntu 18.04 LTS 이상, CentOS 7 이상, Debian 9 이상 등)

## Getting Started

### 사전 요구사항

> [!Note]
> 이 프로젝트는 Docker와 Docker Compose를 사용하여 로컬 환경에서 쉽게 실행할 수 있도록 구성되어 있습니다.  
> 다음 단계를 따라 프로젝트를 설정하고 실행하세요.   
> Docker 설치 방법은 [Docker 공식 문서](https://docs.docker.com/desktop/)를 참조하세요.
 
### **설치 및 실행 단계**

1. **프로젝트 클론**

   Git을 사용하여 이 프로젝트를 로컬 시스템으로 클론합니다.
    ```bash
    git clone https://github.com/dealim/voice-doctor
    cd voice-doctor
    ```

3. **구글 클라우드 서비스키 설정**
   
    **[서비스키 적용]**
    ```bash
    cd keys
    vi secrets.json
    ```
    공식문서를 따라 발급받은 키들을 적용해야합니다. `keys` 폴더에 secrets.json 파일을 생성하고 다음과 같이 입력합니다.  
    ```
    {
    "APIKEY_TEXT_EMOTION_ANALYSIS" : "서비스키 파일명",
    "HEALTH": "서비스키 파일명",
    "OCR": "서비스키 파일명",
    "STT": "서비스키 파일명",
    "VERTEX_AI": "서비스키 파일명"
    }
    ```
    프로젝트의 `keys`폴더에 발급받은 서비스키를 저장한뒤, 파일명을 맞춰 "서비스키 파일명"을 채워주세요.

5. **Docker 이미지 빌드 및 컨테이너 실행**

   Docker Compose를 사용하여 서비스를 빌드하고 실행합니다.
    ```bash
    docker-compose up --build
    ```
   빌드가 완료되고 컨테이너가 실행되면, Flask 애플리케이션과 Nginx 서버가 시작됩니다.


6. **웹사이트 접속**
   
   브라우저를 열고 `http://localhost:10100`로 접속합니다. 애플리케이션의 홈페이지가 표시됩니다.

## Architecture

![](./assets/아키텍처.png)

## Folder Structure

```
voice-doctor/
│
├── static/                 
│   ├── css/                                    # CSS 파일들
│   ├── js/                                     # JavaScript 파일들
│   └── images/                                 # 이미지 파일들
│
├── templates/               
│   ├── index.html                              # index 페이지
│   ├── main_page.html                          # 메인 화면
│   ├── show_text_emotion_analysis.html         # 감정분석 결과 페이지
│   └── show_text_summary.html                  # 환자 녹음 내용 요약, 키워드 정확도
│
├── services/                                   # 비즈니스 로직
│   ├── settings.py                             # 프로젝트명, 키설정
│   ├── sound_to_text.py                        # STT 구현, json 반환
│   ├── summary.py                              # 텍스트 요약, 키워드 분석, json 반환
│   ├── text_emotion_analysis.py                # 감정분석, json 반환
│   └── voice
│       ├── [음성 파일 이름]_stt.json  
│       ├── [음성 파일 이름]_health_response.json
│       └── [음성 파일 이름].flac  
│
├── app.py                                      # Flask 앱의 메인 실행 파일
├── config.py                                   # 애플리케이션 설정 / 이것도 없어도 됨
├── .env                                        # 환경 변수 파일
├── Dockerfile                                  # 컨테이너 환경
├── docker-compose.yml                          # nginx + flask 서버
└── requirements.txt                            # 프로젝트 의존성 목록 파일
```

## Roles

[팀원 역할](./docs/ROLES.md)

## Demo Video
[![Video Label](http://img.youtube.com/vi/4RMyuYGm1PM/0.jpg)](https://youtu.be/4RMyuYGm1PM)

## License
MIT License

Copyright (c) 2023 dealim
