from flask import Flask, request, current_app, send_from_directory
from flask_restful import Resource,Api
from vits.tts_api import build_wav
import os

app = Flask(__name__)
api = Api(app)

current_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".") + "/"
app.config['WAV_FOLDER'] = os.path.join(current_path, 'wavs/')

class Vits(Resource):
    def get(self):
        index = int(request.args.get('index'))
        text = request.args.get('text')
        wav_path = os.path.join(app.config['WAV_FOLDER'], 'cache.wav')
        build_wav(index, text, wav_path)
        return send_from_directory(current_app.config['WAV_FOLDER'],'cache.wav',as_attachment=True)

api.add_resource(Vits, '/vits')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5123)