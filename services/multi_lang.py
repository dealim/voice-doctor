from google.cloud import speech_v1p1beta1 as speech
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(parent_dir, "keys/applicationteam02-cf34308f779b.json")
speech_file = "voice/english.flac"
def multi_transcribe_audio(filename):

    client = speech.SpeechClient()

    # 언어는 기본 언어를 포함하여 최대 4개의 언어를 지원한다.
    first_lang = "en-US"
    alternate_languages = ["ko-KR", "ja-JP"]
    with open(filename, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        # encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=24000,
        audio_channel_count=1,
        language_code=first_lang,
        alternative_language_codes=alternate_languages,
    )

    print("Waiting for operation to complete...")
    response = client.recognize(config=config, audio=audio)

    for i, result in enumerate(response.results):
        print("result : ",result)
        alternative = result.alternatives[0]
        print("-" * 20)
        print(f"First alternative of result {i}: {alternative}")
        print(f"Transcript: {alternative.transcript}")

    return response.results

def detect_language():
    lang_code = multi_transcribe_audio(speech_file)
    for i, result in enumerate(lang_code):

        language_check = result.language_code
    return language_check



detect_lang = detect_language()
print(detect_lang)



