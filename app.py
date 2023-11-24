from flask import Flask, render_template, request, jsonify
from services.text_emotion_analysis import json_analyze_sentiment
from services.sound_to_text import transcribe_audio
from services.summary import json_summary
import os
import json

app = Flask(__name__)
current_dir = os.path.dirname(os.path.abspath(__file__))
voice_dir = os.path.join(current_dir,'services/voice')

# Root page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/main')
def main_page():
    return render_template('main_page.html')


@app.route('/show/voicetext')
def show_voicetext():
    return render_template('show_text_summary.html')


@app.route('/get/voicetext')
def get_voicetext():
    json_file_name = 'summary.json'
    file_path = os.path.join(voice_dir, json_file_name)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        return jsonify(json_data)
    else:
        return jsonify({"error": "File not found"}), 404


@app.route('/show/emotion')
def show_emotion():
    json_file_name = 'stt.json'
    # 환자용 JSON 파일 읽기 & 각 문장에 대해 감정 분석 수행
    patient = json_analyze_sentiment(os.path.join(voice_dir, json_file_name))

    return render_template('show_text_emotion_analysis.html', patient=patient[0])

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        filename = file.filename

        # 파일 저장 경로 설정
        save_path = os.path.join(voice_dir, filename)
        file.save(save_path)

        # ~.flac을 stt.json으로 변환
        transcribe_audio(save_path, os.path.join(voice_dir, 'stt.json'))

        # stt.json을 summary.json으로 변환
        json_summary(os.path.join(voice_dir, 'stt.json'))

        return jsonify({'message': 'File uploaded successfully!', 'filename' : filename})
    else:
        return jsonify({'message': 'No file part'})

# execute app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10100, debug=True)
