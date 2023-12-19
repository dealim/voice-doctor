from google.cloud import speech_v1
from google.cloud import speech_v1p1beta1 as speech
from pydub.utils import mediainfo
import io
import os
import time
import json
from flask import current_app

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(parent_dir, "keys/applicationteam02-cf34308f779b.json")


def multi_transcribe_audio(filename, extname):
    client = speech.SpeechClient()
    file_path = os.path.join(current_dir, 'voice', filename)
    audio_info = mediainfo(file_path)
    sample_rate = int(audio_info['sample_rate'])
    start_time = time.time()
    if (extname == 'wav'):
        file_encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16
    elif (extname == 'flac'):
        file_encoding = speech.RecognitionConfig.AudioEncoding.FLAC

    # 언어는 기본 언어를 포함하여 최대 4개의 언어를 지원한다.
    first_lang = "en-US"
    alternate_languages = ["ko-KR", "ja-JP"]
    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=file_encoding,
        sample_rate_hertz=sample_rate,
        audio_channel_count=1,
        language_code=first_lang,
        alternative_language_codes=alternate_languages,
    )

    response = client.recognize(config=config, audio=audio)
    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]

        language_check = result.language_code

    current_app.logger.info("언어 인식 완료")
    return file_encoding, sample_rate, language_check, content


def transcribe_audio(filename, output_json_file, extname):
    file_encoding, sample_rate, language_check, content = multi_transcribe_audio(filename, extname)

    client = speech_v1.SpeechClient()

    audio = {"content": content}
    if (file_encoding == speech.RecognitionConfig.AudioEncoding.LINEAR16):
        encoding = 'LINEAR16'
    elif (file_encoding == speech.RecognitionConfig.AudioEncoding.FLAC):
        encoding = 'FLAC'
    print("language_check : ",language_check)
    if language_check == "en-US":
        config = {
            "language_code": language_check,
            "model": "medical_dictation",
            "encoding": encoding,
            "sample_rate_hertz": sample_rate
        }

    elif language_check == "ko-KR" or "ja-JP":
        config = {
            "language_code": language_check,
            "encoding": encoding,
            "sample_rate_hertz": sample_rate
        }

    response = client.recognize(config=config, audio=audio)
    save_response_as_json(response, output_json_file)

    # print(f"json 파일 생성 완료: {output_json_file}")


def save_response_as_json(response, output_file):
    results = []
    for result in response.results:
        alternative = result.alternatives[0]
        print(result.language_code)
        results.append({
            "transcript": alternative.transcript,
            "confidence": alternative.confidence,
            "language_code": result.language_code
        })

    with io.open(output_file, 'w') as json_file:
        json.dump(results, json_file, indent=4)