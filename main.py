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
    ])

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    # Railway sets $PORT automatically — do NOT use 5000 fallback!
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port)
