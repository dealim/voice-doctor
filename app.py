from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# Root page
@app.route('/')
def index():
    return render_template('index.html')

# Example outher page
@app.route('/other')
def other():
    return render_template('other.html')

# Example API endpoint
@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    if request.method == 'POST':
        # Process the POST request
        data = request.json
        # Process data...
        return jsonify({'message': 'Data received', 'data': data})
    else:
        # Handle GET request
        return jsonify({'message': 'Send some data'})


# execute app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10100)
