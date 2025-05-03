from flask import Flask, request, send_file
import os
import subprocess

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    input_path = '/tmp/input.mp4'
    output_path = '/tmp/output.mp3'
    file.save(input_path)

    subprocess.run([
        'ffmpeg', '-i', input_path,
        '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k',
        output_path
    ], check=True)

    return send_file(output_path, as_attachment=True)
