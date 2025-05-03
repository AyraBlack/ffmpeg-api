from flask import Flask, request, send_file
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    input_file = request.files['file']
    input_path = f"/tmp/{uuid.uuid4()}.mp4"
    output_path = input_path.replace('.mp4', '.mp3')

    input_file.save(input_path)

    try:
        subprocess.run(['ffmpeg', '-i', input_path, output_path], check=True)
        return send_file(output_path, mimetype='audio/mpeg')
    except subprocess.CalledProcessError:
        return 'Conversion failed', 500
    finally:
        os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
