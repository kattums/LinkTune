from flask import Flask, request, render_template
from linktune.api.convert import Convert

app = Flask(__name__, static_folder='static')

# Set up route handlers
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/convert')
def convert():
    print('convert request received')
    url = request.args.get('url')
    target_service = request.args.get('target_service')
    return Convert().convert_link(url, target_service)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)