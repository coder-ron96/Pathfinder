# app.py

from flask import Flask, jsonify
from flask_cors import CORS  # This allows cross-origin requests from your HTML page

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/run-pathfinder', methods=['GET'])
def run_pathfinder():
    result = "Pathfinder result goes here"  # Replace with your actual Pathfinder logic if needed
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
