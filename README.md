# GCP-TEAM2 😃
[노션](https://far-fossa-e64.notion.site/94272df5c9344a48bc73169efd122623?pvs=4)

```
GCP-TEAM2/
│
├── static/                 
│   ├── css/                 # CSS 파일들
│   ├── js/                  # JavaScript 파일들
│   └── images/              # 이미지 파일들
│
├── templates/               
│   ├── index.html           # 메인 페이지 템플릿
│   └── other.html           # 다른 페이지 템플릿들
│
├── venv/                    # 가상 환경 폴더
│
├── services/                # 비즈니스 로직
│   ├── emotion_analysis.py  # 감정 분석 로직
│   ├── text_processing.py   # 텍스트 처리 및 요약
│   ├── image_processing.py  # 이미지 처리 및 감정 분석
│   └── health_prediction.py # 건강 지표 예측 로직
│
├── models/                  # 데이터 모델 / 모델은 없이 해도 될듯
│   ├── patient.py           # 환자 관련 모델
│   └── session.py           # 세션/대화 관련 모델
│
├── utils/                   # 유틸리티 함수 및 클래스
│   └── helpers.py           # 도우미 함수들
│
├── app.py                   # Flask 앱의 메인 실행 파일
├── config.py                # 애플리케이션 설정 / 이것도 없어도 됨
├── .env                     # 환경 변수 파일
├── Dockerfile               # 컨테이너 환경
├── docker-compose.yml       # 같이 실행될 DB서버 있으면 작성
└── requirements.txt         # 프로젝트 의존성 목록 파일
```
