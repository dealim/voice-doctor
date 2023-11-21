import requests
import os

# 서비스 계정 키(JSON 파일)의 경로
service_account_key = "/Users/yuhyerin/PycharmProjects/STT_test/appteam2-b11b34493f7a.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_key

url = "https://speech.googleapis.com/v1/speech:recognize"

# 요청 헤더 설정
headers = {
    "Content-Type": "application/json; charset=utf-8"
    # "Authorization": f"Bearer {service_account_key}"
}


# JSON payload 작성
payload = {
    "config": {
        "languageCode": "en-US",
        "encoding": "LINEAR16",
        "model": "medical_conversation"
    },
    "audio": {
        "uri": "file://Users/yuhyerin/PycharmProjects/STT_test/speech_medical_conversation_2.wav"
    }
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())

