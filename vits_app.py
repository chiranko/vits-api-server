import os
import sys

current_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".") + "/"
sys.path.append(current_path)

from flask import Blueprint, request, send_from_directory
from flask_restful import Resource,Api
from vits.tts_api import TTS_Model

vits_app = Blueprint("vits", __name__)
api = Api(vits_app)

wave_folder = os.path.join(current_path, 'wavs/')
if not os.path.isdir(wave_folder):
    os.makedirs(wave_folder)

model_names = ["yuzusoft", "tsukiniyori"]
models = {}

for model in model_names:
    models[model] = TTS_Model(model)

class Vits(Resource):
    def get(self):
        model = request.args.get('model')
        index = int(request.args.get('index'))
        text = request.args.get('text')
        wav_path = os.path.join(wave_folder, 'cache.wav')
        models[model].build_wav(index, text, wav_path)
        return send_from_directory(wave_folder,'cache.wav',as_attachment=True)

api.add_resource(Vits, '')
