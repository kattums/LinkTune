from flask import Flask, request
from linktune.api.convert import Convert

app = Flask(__name__)

# Set up route handlers
@app.route('/')
def index():
    return 'Bojangles'

@app.route('/convert')
def convert():
    url = request.args.get('url')
    target_service = request.args.get('target_service')
    return Convert().convert_link(url, target_service)

if __name__ == '__main__':
    app.run(debug=True)