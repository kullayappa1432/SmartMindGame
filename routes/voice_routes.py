
from flask import Blueprint
import subprocess

voice_bp = Blueprint('voice', __name__)

@voice_bp.route('/start-voice')
def start():
    subprocess.Popen(['python', 'modules/voice/voice_control.py'])
    return {"status":"voice started"}
