from google.cloud import speech_v1
from google.cloud import speech_v1p1beta1 as speech
from pydub.utils import mediainfo
import io
import os
import time
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(parent_dir, "keys/applicationteam02-cf34308f779b.json")

def multi_transcribe_audio(filename, extname):
    client = speech.SpeechClient()
    file_path = os.path.join(current_dir, 'voice', filename)
    audio_info = mediainfo(file_path)
    sample_rate = int(audio_info['sample_rate'])
    if (extname == 'wav'):
        encoding = 'speech.RecognitionConfig.AudioEncoding.LINEAR16'
    elif (extname == 'FLAC'):
        encoding = 'speech.RecognitionConfig.AudioEncoding.FLAC'

    # 언어는 기본 언어를 포함하여 최대 4개의 언어를 지원한다.
    first_lang = "en-US"
    alternate_languages = ["ko-KR", "ja-JP"]
    with open(filename, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate,
        audio_channel_count=1,
        language_code=first_lang,
        alternative_language_codes=alternate_languages,
    )
    print("Waiting for operation to complete...")
    response = client.recognize(config=config, audio=audio)
    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        # print("-" * 20)
        # print(f"First alternative of result {i}: {alternative}")
        # print(f"Transcript: {alternative.transcript}")

    return response.results, encoding, sample_rate

def detect_language(lan_result):

    lang_code = multi_transcribe_audio()
    for i, result in enumerate(lang_code):

        language_check = result.language_code
    return "language_check"
multi_lan = multi_transcribe_audio()
detect_lang = detect_language(multi_lan)
print(detect_language(multi_lan))

def transcribe_audio(filename, output_json_file, extname):
    multi_lan = multi_transcribe_audio()
    detect_lang = detect_language(multi_lan)

    client = speech_v1.SpeechClient()
    # start_time = time.time()
    with open(multi_lan.filename, "rb") as audio_file:
        content = audio_file.read()

    audio = {"content": content}
    if (multi_lan.extname == 'speech.RecognitionConfig.AudioEncoding.LINEAR16'):
        encoding = 'LINEAR16'
    elif (multi_lan.extname == 'speech.RecognitionConfig.AudioEncoding.FLAC'):
        encoding = 'FLAC'

    if detect_lang == "en-US":
        config = {
            "language_code": detect_lang,
            "model": "medical_dictation",
            "encoding": encoding,
            "sample_rate_hertz": multi_lan.sample_rate
        }

    elif detect_lang == "ko-KR" or "ja-JP":
        config = {
            "language_code": detect_lang,
            "encoding": encoding,
            "sample_rate_hertz": multi_lan.sample_rate
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
