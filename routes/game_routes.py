
from flask import Blueprint
import subprocess

game_bp = Blueprint('game', __name__)

@game_bp.route('/start-game')
def start():
    subprocess.Popen(['python', 'modules/gesture/gesture_game.py'])
    return {"status":"game started"}
