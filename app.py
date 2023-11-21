from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')


# Root page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show/voicetext', methods=['GET'])
def show_voicetext():
    return render_template('show_text_summary.html')


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
