from google.cloud import speech_v1
import io
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(parent_dir, "keys/applicationteam02-cf34308f779b.json")

def transcribe_audio(file_path, output_json_file):
    client = speech_v1.SpeechClient()

    start_time = time.time()

    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = {"content": content}

    config = {
        "language_code": "en-US",
        "model": "medical_conversation",
        "encoding": "FLAC",
        "sample_rate_hertz": 48000
    }

    response = client.recognize(config=config, audio=audio)
    save_response_as_json(response, output_json_file)

    print(f"json 파일 생성 완료: {output_json_file}")


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


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            filename = event.src_path
            print(f"새 파일이 생성되었습니다: {filename}")
            if filename.endswith('.flac') and not filename.endswith('.json'):
                output_json_file = filename.rsplit('.', 1)[0] + ".json"
                transcribe_audio(filename, output_json_file)
            # elif filename.endswith('.json'):
            #     # .json 파일이 생성되면 변환 과정은 수행하지 않고 로그만 출력
            #     print("json 파일이 이미 생성되었습니다.")


if __name__ == "__main__":
    folder_to_watch = current_dir + '/voice'

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=folder_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
