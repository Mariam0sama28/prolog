from flask import Flask, request, jsonify
from flask_cors import CORS
from frontend import bp as frontend_bp

app = Flask(__name__)
CORS(app)

tasks = []

app.register_blueprint(frontend_bp) 

@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.json
    tasks.append({ "name": data['name'],
      "priority": data['priority'],
      "duration": data['duration'],
      "finished": False})
    return jsonify({"message": "Task added successfully!"})

@app.get('/debug')
def deg():
    print('tt')
    return jsonify({"message": "Task added successfully!"})

@app.route("/get_tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

if __name__ == "__main__":
    app.run(port=5000)
