from flask import Flask, render_template, request, jsonify, session, send_from_directory
from services.text_emotion_analysis import get_json_sentiment
from services.sound_to_text import transcribe_audio
from services.summary import text_summarization
import os
import json

app = Flask(__name__)

app.secret_key = os.urandom(24)
current_dir = os.path.dirname(os.path.abspath(__file__))
voice_dir = os.path.join(current_dir,'services/voice')
stt_name = ''

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
    filename = session.get('uploadedFileName')
    json_file_name = filename + '_health_response.json'
    file_path = os.path.join(voice_dir, json_file_name)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        return jsonify(json_data)
    else:
        return jsonify({"error": "File not found"}), 404


@app.route('/show/emotion')
def show_emotion():
    return render_template('show_text_emotion_analysis.html')


@app.route('/get/emotion')
def get_emotion():
    filename = session.get('uploadedFileName')
    json_file_name = filename + '_emotion.json'
    file_path = os.path.join(voice_dir, json_file_name)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        return jsonify(json_data)
    else:
        return jsonify({"error": "File not found"}), 404


@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        filename = file.filename
        filerleftname = filename.rsplit('.')[0]
        session['uploadedFileName'] = filerleftname

        # 파일 저장 경로 설정
        save_path = os.path.join(voice_dir, filename)
        file.save(save_path)

        # ~.flac을 [파일이름]_stt.json으로 변환
        stt_name = filerleftname +'_stt.json'
        transcribe_audio(filename, save_path, os.path.join(voice_dir, stt_name))

        # JSON 파일 읽기
        with open(os.path.join(voice_dir, stt_name), 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            text = json_data[0]['transcript']

        # stt.json을 [파일이름]_emotion.json 으로 변환
        get_json_sentiment(os.path.join(voice_dir, filerleftname + '_stt.json'), filerleftname)

        # stt.json을 [파일이름]_health_response.json 으로 변환
        file_health_response = filerleftname + '_health_response.json'
        text_summarization(file_health_response,0.0, 'applicationteam02', 'us-central1', text);

        return jsonify({'message': 'File uploaded successfully!', 'filename' : filename})
    else:
        return jsonify({'message': 'No file part'})

@app.route('/audio/<filename>')
def download_file(filename):
    print(filename)
    return send_from_directory('assets', filename)

# execute app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10100, debug=True)
