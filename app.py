from flask import Flask, render_template, jsonify
import redis

app = Flask(__name__)


@app.route('/connect', methods=['GET'])
def connect_redis():
    try:
        r = redis.Redis(host='192.168.0.115', port=6379, db=0)
        r.ping()
        return jsonify({'status': 'success', 'message': 'Connected to Redis successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
