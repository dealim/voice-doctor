from google.cloud import speech_v1
import io

# 서비스 계정 키(JSON 파일)의 경로를 환경 변수로 설정
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/yuhyerin/PycharmProjects/STT_test/applicationteam02-cf34308f779b.json"

def transcribe_audio(file_path):
    client = speech_v1.SpeechClient()

    # 오디오 파일 읽기
    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = {"content": content}

    config = {
        "language_code": "en-US",
        "model": "medical_conversation",
        "encoding": "LINEAR16",
    }

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))


if __name__ == "__main__":
    audio_file_path = "/Users/yuhyerin/PycharmProjects/STT_test/speech_medical_conversation_2.wav"
    transcribe_audio(audio_file_path)
