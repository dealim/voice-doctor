# 베이스 이미지 설정 (Python 3.9을 사용)
FROM python:3.9

# FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:latest

# 애플리케이션 폴더 생성
WORKDIR /app

# 애플리케이션 종속성 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 코드 복사
COPY . /app

# Flask 애플리케이션 실행
CMD ["python", "app.py"]