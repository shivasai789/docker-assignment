from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["test"]
collection = db["submissions"]

@app.route('/')
def home():
    return "Hii, from backend!"

@app.route('/process-form', methods=['POST'])
def process_form():
    try:
        data = request.get_json()

        # Validate required fields
        if not all(k in data for k in ['name', 'email', 'message']):
            return jsonify({"error": "Missing required fields", "status": "error"}), 400

        # Append metadata
        data['timestamp'] = datetime.now().isoformat()

        # Insert into MongoDB
        result = collection.insert_one(data)

        response = {
            "message": f"Thank you {data['name']}! Your details has been saved.",
            "submission_id": str(result.inserted_id),
            "status": "success",
            "timestamp": data['timestamp']
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/submissions', methods=['GET'])
def get_submissions():
    try:
        submissions = list(collection.find({}, {'_id': 0}))  
        return jsonify({
            "count": len(submissions),
            "submissions": submissions,
            "status": "success"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
