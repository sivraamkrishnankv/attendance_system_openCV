from flask import Flask, render_template
import subprocess
import os
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_camera', methods=['POST'])
def start_camera():
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mainfe.py')
    try:
        process = subprocess.Popen([sys.executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            return 'Camera started'
        else:
            return f'Error: {stderr.decode()}'
    except Exception as e:
        return f'Exception: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
