
from flask import Blueprint
import subprocess

gesture_bp = Blueprint('gesture', __name__)

@gesture_bp.route('/start-gesture')
def start():
    subprocess.Popen(['python', 'modules/gesture/gesture_mouse.py'])
    return {"status":"gesture started"}
