#FROM python:3.9

FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:latest

# 파이썬 설치
RUN apt-get update && apt-get install -y python3.9 python3-pip

# 애플리케이션 폴더 생성
WORKDIR /app

# 애플리케이션 종속성 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 코드 복사
COPY . /app

# Flask 애플리케이션 실행
CMD ["python", "app.py"]