from flask import Flask, render_template, request, jsonify, session, send_from_directory
from services.text_emotion_analysis import get_json_sentiment
from services.speech_to_text import transcribe_audio
from services.summary import text_summarization
from services.vertexai_text_command import text_generation
from services.document_ai_ocr import process_document
import os
import json

app = Flask(__name__)

app.secret_key = os.urandom(24) # 세션을 위한 비밀키 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
voice_dir = os.path.join(current_dir,'services','voice')

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
        text_summarization(file_health_response,0.0, 'applicationteam02', 'us-central1', text)
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

#### 임의로 만들었습니다. (mj) ### 
    """pdf filename -> process_document()로 pdf에서 text 추출하는 ocr 진행 -> vertex ai 모델로 text에서 원하는 것들 명령함

    Returns:
        html : 예시로 결과 보여주는 html,
        str : 확인용 pdf path
        str : 3줄 요약, 
        json : 특정 정보 추출 후 json 생성, 
    """
@app.route('/questionnaire/ocr', methods=['GET'])
def questionnaire_ocr():
    # 문진표 파일 정보 
    filename = "questionnaire_english.pdf"
    file_path = os.path.join(current_dir, "assets", filename)

    # 문진표 OCR 진행
    text = process_document(file_path=file_path, mime_type='application/pdf')
    app.logger.info("OCR완료")
    
    # OCR 진행한 파일에서 3줄 요약
    doc_summary_command = """Provide a summary for the following conversation in three sentences:"""
    doc_summary_result = text_generation(0.0, 'us-central1', text, doc_summary_command)
    app.logger.info("OCR에서 3줄 요약 완료")
    
    # OCR 진행한 파일에서 특정 정보 추출
    doc_info_export_command = """Please compile information pertaining to \
            'NAME, DATE OF SERVICE, DATE OF BIRTH, DOCTOR, PATIENT, CHIEF COMPLAINT, ONSET OF SYMPTOMS, \
            MECHANISM OF INJURY, What makes the pain better?, What makes the pain worse?' \
            and Pair each key with its corresponding value and format it in JSON:"""  
    doc_info_export_result = text_generation(0.0, 'us-central1', text, doc_info_export_command)
    # 텍스트를 JSON으로 변환
    doc_info_export_result_json = json.loads(doc_info_export_result.replace('json', '').replace("```", ''))
    app.logger.info("OCR에서 특정 정보 추출 완료")
    
    """ pdf 확인용 : 추후에 병합할 때는 다음 부분을 삭제해 주세요.
    파일 삭제 : static/images/questionnaire_english.pdf
    코드 삭제 : pdf_path 관련 코드 (아래 2개)
    """
    pdf_path ="images/" + filename
    return render_template('questionnaire.html', pdf_path=pdf_path, doc_summary_result=doc_summary_result, doc_info_export_result_json=doc_info_export_result_json)

# execute app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10100, debug=True)
