from google.cloud import speech_v1
from pydub.utils import mediainfo
import io
import os
import time
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(parent_dir, "keys/applicationteam02-cf34308f779b.json")


def transcribe_audio(filename, file_path, output_json_file):
    client = speech_v1.SpeechClient()
    file_path = os.path.join(current_dir, 'voice', filename)
    audio_info = mediainfo(file_path)
    sample_rate = int(audio_info['sample_rate'])
    start_time = time.time()

    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = {"content": content}

    config = {
        "language_code": "en-US",
        "model": "medical_dictation",
        "encoding": "LINEAR16",
        "sample_rate_hertz": sample_rate
    }

    response = client.recognize(config=config, audio=audio)
    save_response_as_json(response, output_json_file)

    # print(f"json 파일 생성 완료: {output_json_file}")

def save_response_as_json(response, output_file):
    results = []
    for result in response.results:
        alternative = result.alternatives[0]
        results.append({
            "transcript": alternative.transcript,
            "confidence": alternative.confidence
        })

    with open(output_file, 'w') as json_file:
        json.dump(results, json_file, indent=4)
