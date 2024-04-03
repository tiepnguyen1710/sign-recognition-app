from flask import Flask, request, jsonify
import json
from data_model import DataModel

app = Flask(__name__)

@app.route('/api/data', methods=['POST'])
def receive_data():
    if request.method == 'POST':
        data = request.json
        
        if data:
            
            print(data["data"])
            
            return jsonify({'message': 'Data received successfully'}), 200
        else:
            return jsonify({'error': 'No data provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
