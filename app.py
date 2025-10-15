# app.py
from flask import Flask, request, jsonify
from test import process_data
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "python-api"})

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.get_json()
        if not data or 'input' not in data:
            return jsonify({"error": "Missing 'input' in request body"}), 400
        
        # Call your function from test.py
        result = process_data(data['input'])
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Python API is running!", "version": "1.0"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
