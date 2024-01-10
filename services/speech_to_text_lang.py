from google.cloud import speech_v1
from google.cloud import speech_v1p1beta1 as speech
from pydub.utils import mediainfo
import io
import os
import time
import json
from flask import current_app
from .settings import get_projectId, get_secret

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_secret("STT")

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

    if language_check == "en-us" or language_check == "ja-jp":
        config = {
            "language_code": language_check,
            # "model": "medical_dictation",
            "encoding": encoding,
            "sample_rate_hertz": sample_rate,
            "enable_automatic_punctuation" : True,
            "use_enhanced" : True,
            # A model must be specified to use enhanced model.
            "model" : "phone_call"
        }


    elif language_check == "ko-kr":
        config = {
            "language_code": language_check,
            "encoding": encoding,
            "sample_rate_hertz": sample_rate,
            "enable_automatic_punctuation": True,
            "use_enhanced": True,
            # A model must be specified to use enhanced model.
            "model" : "telephony"
            # "model": "latest_long"
        }


    print("config : ", config)
    response = client.recognize(config=config, audio=audio)
    save_response_as_json(response, output_json_file)

    # print(f"json 파일 생성 완료: {output_json_file}")


def save_response_as_json(response, output_file):
    combined_transcript = ''
    combined_confidence = 0
    num_results = 0

    for result in response.results:
        alternative = result.alternatives[0]
        combined_transcript += alternative.transcript + ' '
        combined_confidence += alternative.confidence
        num_results += 1

    if num_results > 0:
        combined_confidence /= num_results  # 평균 신뢰도 계산

    combined_result = {
        "transcript": combined_transcript.strip(),
        "confidence": combined_confidence,
        "language_code": response.results[0].language_code if num_results > 0 else None
    }

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump([combined_result], json_file, ensure_ascii=False, indent=4)
