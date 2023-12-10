from flask import Flask, render_template, request, jsonify, session, send_from_directory
from services.text_emotion_analysis import get_json_sentiment
from services.speech_to_text import transcribe_audio
from services.summary import text_summarization
import os
import json

app = Flask(__name__)

app.secret_key = os.urandom(24) # 세션을 위한 비밀키 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
voice_dir = os.path.join(current_dir,'services/voice')

# Root page
@app.route('/')
def index():
    return render_template('index.html')

# 동적 메인 페이지
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
        # 파일에 대한 이름 처리
        file = request.files['file']
        filename = file.filename
        fileleftname = filename.rsplit('.')[0]
        session['uploadedFileName'] = fileleftname

        # 파일 저장 경로 설정
        save_path = os.path.join(voice_dir, filename)
        file.save(save_path)
        app.logger.info(fileleftname + ".flac 파일이 서버에 저장됨")

        # ~.flac을 [파일이름]_stt.json으로 변환
        stt_name = fileleftname +'_stt.json'
        transcribe_audio(filename, save_path, os.path.join(voice_dir, stt_name))
        app.logger.info(stt_name + " : stt 완료")

        # JSON 파일 읽기
        with open(os.path.join(voice_dir, stt_name), 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            text = json_data[0]['transcript']

        # stt.json을 분석후 [파일이름]_emotion.json 으로 변환
        emotion_name = fileleftname + '_stt.json'
        get_json_sentiment(os.path.join(voice_dir, emotion_name), fileleftname)
        app.logger.info(emotion_name + " : 감정 분석 완료")

        # stt.json을 분석후 [파일이름]_health_response.json 으로 변환
        file_health_response = fileleftname + '_health_response.json'
        text_summarization(file_health_response,0.0, 'applicationteam02', 'us-central1', text);
        app.logger.info(file_health_response + " : 헬스케어 요약 완료")

        return jsonify({'message': 'File uploaded successfully!', 'filename' : filename})
    else:
        return jsonify({'message': 'No file part'})

@app.route('/api/record', methods=['POST'])
def upload_record():
    if 'audio' in request.files:
        audio_file = request.files['audio']

        # 파일 저장
        filepath = os.path.join(voice_dir, audio_file.filename)
        audio_file.save(filepath)

        # 파일 분석 로직
        return jsonify({'message' : 'File uploaded successfully!'})
    return jsonify({'message' : 'upload failed'})

@app.route('/audio/<filename>')
def download_file(filename):
    return send_from_directory('assets', filename)

# execute app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10100, debug=True)
