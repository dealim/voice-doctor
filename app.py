from flask import Flask, render_template, request, jsonify
from services.text_emotion_analysis import json_analyze_sentiment
from services.merge_real_final import transcribe_audio
import os
import json

app = Flask(__name__)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Root page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/main')
def main_page():
    return render_template('main_page.html')


@app.route('/show/voicetext')
def show_voicetext():
    # filename = request.cookies.get('uploadedFileName', None)
    # transcribe_audio(current_dir + '/services/voice/' + filename, current_dir + '/services/voice/voice.json')
    return render_template('show_text_summary.html')

@app.route('/get/voicetext')
def get_voicetext():
    file_path = current_dir + '/services/voice/voice.json'

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            return jsonify(data)
    else:
        return jsonify({"error": "File not found"}), 404

@app.route('/show/emotion')
def show_emotion():
    # 환자용 JSON 파일 읽기 & 각 문장에 대해 감정 분석 수행
    patient = json_analyze_sentiment('./services/patient_text_request.json')
    # 의사용 JSON 파일 읽기 & 각 문장에 대해 감정 분석 수행
    doctor = json_analyze_sentiment('./services/doctor_text_request.json')

    # print(patient)
    """ 기분 바뀌는지 확인용 (doc_sentiment_score 수치 바꾸면 얼굴 바뀜
    patient = [{
        'doc_sentiment_score': -1,
        'doc_sentiment_magnitude': 2.931999921798706,
        'text_contents': [
            'Good morning.',
            'Uh , sure , so , um , I woke up probably three or four days ago , which , uh , wheezing and short of breath .',
            'I cough infrequently , but no , uh , chest pain .',
            'Uh , no , and I also took a test , which was negative .',
            'Uh , it has been getting a lot worse .',
            'Um , I had a gone hiking , and I got caught in the rain the day before this all started .'
        ],
        'senti_scores': [0.337, -0.671, 0.0, 0.069, -0.952, -0.231],
        'senti_magnitudes': [0.379, 0.724, 0.3, 0.286, 0.987, 0.257]
    }]
    """

    return render_template('show_text_emotion_analysis.html', patient=patient[0], doctor=doctor[0])

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        filename = file.filename
        # 파일 저장 경로 설정
        save_path = os.path.join('services/voice', filename)
        file.save(save_path)
        return jsonify({'message': 'File uploaded successfully!', 'filename' : filename})
    else:
        return jsonify({'message': 'No file part'})

# execute app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10100, debug=True)
