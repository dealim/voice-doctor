from flask import Flask, render_template, request, jsonify, session, send_from_directory
from services.text_emotion_analysis import get_json_sentiment
from services.speech_to_text_lang import transcribe_audio
from services.summary import text_summarization
from services.document_ai_ocr import get_ocr_json
from services.filesave import save_file
from services.vertexai_text_command import text_generation
from config import Config
import os
import uuid
import json

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24) # 세션을 위한 비밀키 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
voice_dir = os.path.join(current_dir,'services','voice')

# Root page
@app.route('/')
def index():
    # 세션 ID 생성 또는 기존 세션 ID 사용
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')

# 동적 메인 페이지
@app.route('/main')
def main_page():
    return render_template('main_page.html')

@app.route('/show/stt')
def show_stt():
    return render_template('show_text_stt.html')

@app.route('/get/stt')
def get_stt():
    session_id = session['session_id']
    json_file_name = session_id + '_stt.json'
    app.logger.info(json_file_name)
    file_path = os.path.join(voice_dir, json_file_name)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        return jsonify(json_data)
    else:
        return jsonify({"error": "File not found"}), 404


@app.route('/show/summary')
def show_summary():
    return render_template('show_text_summary.html')


@app.route('/get/summary')
def get_summary():
    session_id = session['session_id']
    json_file_name = session_id + '_health_response.json'
    app.logger.info(json_file_name)
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
    session_id = session['session_id']
    json_file_name = session_id + '_emotion.json'
    file_path = os.path.join(voice_dir, json_file_name)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        return jsonify(json_data)
    else:
        return jsonify({"error": "File not found"}), 404

@app.route('/show/ocr')
def show_ocr():
    return render_template('show_text_ocr.html')

@app.route('/get/ocr')
def get_ocr():
    session_id = session['session_id']
    json_file_name = session_id + '_ocr.json'
    file_path = os.path.join(voice_dir, json_file_name)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        return jsonify(json_data)
    else:
        return jsonify({"error": "File not found"}), 404

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' in request.files:
            file = request.files['file']
            file_name = file.filename
            session_id = session['session_id']

            # 오디오 파일에 대한 이름처리
            if(file_name=='blob'):
                file_name = f"{session_id}.wav"

            # 파일에 대한 이름 처리
            left_name = file_name.split('.')[0]
            ext_name = file_name.split('.')[1]
            file_name = session_id + '.' + ext_name

            # 파일 저장 경로 설정 및 저장
            save_path = os.path.join(voice_dir, file_name)
            file.save(save_path)
            app.logger.info(file_name + " 파일이 서버에 저장됨")

            # pdf 파일에 대한 처리
            if(ext_name == 'pdf'):
                json_filename = session_id + "_ocr"
                get_ocr_json(file_name, json_filename)
                app.logger.info(json_filename + " : OCR 분석 완료")
                return jsonify({'message': 'File uploaded successfully!', 'file_name': file_name})

            # 보이스 파일을 [session_id]_stt.json으로 변환
            stt_name = session_id +'_stt.json'
            transcribe_audio(file_name, os.path.join(voice_dir, stt_name), ext_name)
            app.logger.info(stt_name + " : stt 완료")

            # stt_json 파일 읽기
            with open(os.path.join(voice_dir, stt_name), 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                # TODO: JSON에 transcript가 정의 되지 않았을 때 오류발생
                text = json_data[0]['transcript']
                language_code = json_data[0]['language_code']

            # stt.json을 분석 후 [파일이름]_emotion.json 으로 변환
            emotion_name = session_id + '_emotion.json'
            get_json_sentiment(os.path.join(voice_dir, stt_name), emotion_name)
            app.logger.info(emotion_name + " : 감정 분석 완료")

            # stt.json을 분석 후 [파일이름]_health_response.json 으로 변환
            file_health_response = session_id + '_health_response.json'
            text_summarization(file_health_response, 0.0, 'us-central1', text, language_code)
            app.logger.info(file_health_response + " : 헬스케어 요약 완료")

            return jsonify({'message': 'File uploaded successfully!', 'file_name': file_name})
        else:
            return jsonify({'message': 'No file part'}), 400
    except Exception as e:
        app.logger.exception("An error occurred during file processing.")
        return jsonify({'message': 'Failed to process the file', 'error': str(e)}), 500


@app.route('/api/record', methods=['POST'])
def upload_record():
    if 'audio' in request.files:
        audio_file = request.files['audio']

        # 세션 ID 생성 또는 기존 세션 ID 사용
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        session_id = session['session_id']

        # 파일 이름 처리
        filename = session_id + ".wav"

        # 파일 경로 설정 및 저장
        filepath = os.path.join(voice_dir, filename)
        audio_file.save(filepath)

        return jsonify({'message': 'File uploaded successfully!'})

    return jsonify({'message': 'upload failed'})

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('assets/demos', filename)

# execute app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10100, debug=True)
