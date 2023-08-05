import os
from flask import Flask, send_file

server = Flask(__name__)

@server.route('/<path:path>')
def mock_service(path=None):
    relpath = path + '.json'
    abspath = os.path.join(os.getcwd(), relpath)
    try:
        result = (send_file(abspath), 200)
    except FileNotFoundError:
        result = ("not found", 404)
    return result

def mock():
    server.run(host='127.0.0.1', port=5000)

if __name__ == '__main__':
    mock()
