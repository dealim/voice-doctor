# _*_ coding: utf-8 _*_

from flask import Flask, request, render_template
import json
from services.text_emotion_analysis import json_analyze_sentiment

app = Flask(__name__)

@app.route('/')
def view():
    # 환자용 JSON 파일 읽기 & 각 문장에 대해 감정 분석 수행
    patient = json_analyze_sentiment('./services/patient_text_request.json')
            
    # 의사용 JSON 파일 읽기 & 각 문장에 대해 감정 분석 수행
    doctor = json_analyze_sentiment('./services/doctor_text_request.json')

    return render_template('chartjs.html', patient=patient[0], doctor=doctor[0])

if __name__ == '__main__':
    app.run()