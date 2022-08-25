from flask import Flask, request, current_app, send_from_directory
from flask_restful import Resource,Api
from vits.tts_api import TTS_Model
import os

app = Flask(__name__)
api = Api(app)

current_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".") + "/"
app.config['WAV_FOLDER'] = os.path.join(current_path, 'wavs/')

model_names = ["yuzusoft", "tsukiniyori"]
models = {}

for model in model_names:
    models[model] = TTS_Model(model)

class Vits(Resource):
    def get(self):
        model = request.args.get('model')
        index = int(request.args.get('index'))
        text = request.args.get('text')
        wav_path = os.path.join(app.config['WAV_FOLDER'], 'cache.wav')
        models[model].build_wav(index, text, wav_path)
        return send_from_directory(current_app.config['WAV_FOLDER'],'cache.wav',as_attachment=True)

api.add_resource(Vits, '/vits')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5123)