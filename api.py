from distutils.log import debug
from fileinput import filename
from flask import *  
from main import *
import os
import ssl
from pydub import AudioSegment
from pydub.utils import make_chunks
from flask_cors import CORS
import io

app = Flask(__name__)  
CORS(app, supports_credentials=True, resources={'*': {'origins': ["https://i9b106.p.ssafy.io", "https://localhost:5173"]}})

@app.route('/classify', methods = ['POST'])  
def success(): 
    if request.method == 'POST': 
        files = os.listdir("wav_storage")
        for file in files:
            os.remove("wav_storage/{}".format(file))

        files = os.listdir("storage")
        for file in files:
            os.remove("storage/{}".format(file))

        f = request.files['file']
        f.save("storage/" + f.filename)

        audioSegment = AudioSegment.from_file("storage/test.webm", 'webm')
        audioSegment.export("wav_storage/plz.wav", format='wav')

        result = main_program()

        return jsonify(result)

@app.route('/combine', methods=['POST'])
def combine_audio():
    id_param = request.args.get('id')
    parts_param = request.args.getlist('parts')
    parts_list = parse_parts_param(parts_param)

    origin_audio = AudioSegment.from_file("file_storage/y"+ id_param +".mp3")
    f = request.files['file']
    f.save("tmp_storage/tmp.webm")

    audioSegment = AudioSegment.from_file("tmp_storage/tmp.webm", 'webm')
    audioSegment.export("dub_storage/user_voice.mp3", format='mp3')
    user_voice = AudioSegment.from_file("dub_storage/user_voice.mp3")

    combined_audio = AudioSegment.silent(duration=0)
    cursor = 0

    for part in parts_list:
        start, end = part
        combined_audio += origin_audio[cursor:start * 100]
        audio_part = user_voice[start * 100:end * 100]
        combined_audio += audio_part
        cursor = end * 100

    combined_audio += origin_audio[cursor:]

    output_file_path = "comb_storage/output_audio.mp3"

    output_buffer = io.BytesIO()
    combined_audio.export(output_buffer, format="mp3")
    output_buffer.seek(0)

    with open(output_file_path, "wb") as output_file:
        output_file.write(output_buffer.read())

    with open(output_file_path, "rb") as output_file:
        audio_data = output_file.read()

    return send_file(output_file_path, as_attachment=True, download_name="audio.mp3")


def parse_parts_param(parts_param):
    parts_list = []
    
    if isinstance(parts_param, list):
        for part in parts_param:
            start, end = map(int, part.split(':'))
            parts_list.append([start, end])
    else:
        parts = parts_param.split(',')
        for part in parts:
            start, end = map(int, part.split(':'))
            parts_list.append([start, end])
    
    return parts_list


if __name__ == '__main__':
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(certfile='../fullchain.pem', keyfile='../privkey.pem')
    app.run(host="0.0.0.0", port=5000, ssl_context=ssl_context)
