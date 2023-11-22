from flask import Flask, render_template, request, jsonify
from services.text_emotion_analysis import json_analyze_sentiment
import os

app = Flask(__name__)
app.config.from_object('config.Config')


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


@app.route('/show/emotion')
def show_emotion():
    # 환자용 JSON 파일 읽기 & 각 문장에 대해 감정 분석 수행

    patient = json_analyze_sentiment('./services/patient_text_request.json')

    # 의사용 JSON 파일 읽기 & 각 문장에 대해 감정 분석 수행
    doctor = json_analyze_sentiment('./services/doctor_text_request.json')

    return render_template('show_text_emotion_analysis.html', patient=patient[0], doctor=doctor[0])


@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        filename = file.filename
        # 파일 저장 경로 설정
        save_path = os.path.join('services/voice', filename)
        file.save(save_path)
        return jsonify({'message': 'File uploaded successfully!'})
    else:
        return jsonify({'message': 'No file part'})

# execute app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10100)
