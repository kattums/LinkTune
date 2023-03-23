from flask import Flask, request, render_template
from linktune.api.convert import Convert

app = Flask(__name__, static_folder='static')
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Set up route handlers
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert')
def convert():
    print('convert request received')
    url = request.args.get('url')
    return Convert().convert_link(url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    