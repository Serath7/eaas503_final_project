from flask import Flask, request, jsonify
from flask_cors import CORS
import database
import manage
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

database.create_db_table()

genres = {
    'metal': 0, 
    'disco': 1,
    'classical': 2, 
    'hiphop': 3, 
    'jazz': 4, 
    'country': 5, 
    'pop': 6, 
    'blues': 7, 
    'reggae': 8, 
    'rock': 9
}

@app.route('/api/search', methods=['GET'])
def api_get_search():
    return jsonify(database.get_search_historys())

@app.route('/api/search',  methods = ['POST'])
def api_add_user():
    user = request.get_json()
    res = manage.run(user['path'],genres)
    database.insert_search_history({
        "file_name": user['path'],
        "result" : res['result']
    })
    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True)
    app.run()