
from flask import Blueprint, jsonify, request
from flask_login import login_required
import subprocess

game_bp = Blueprint('game', __name__)

# Global process reference
game_process = None
current_game_mode = "medium"

@game_bp.route('/start-game', methods=['POST'])
@login_required
def start_game():
    """Start the gesture-based game system"""
    global game_process, current_game_mode
    try:
        # Get game mode from request
        data = request.get_json() or {}
        current_game_mode = data.get('mode', 'medium')
        
        if game_process is None or not game_process.poll() is None:
            # Start game with mode parameter
            game_process = subprocess.Popen(
                ['python', 'modules/gesture/gesture_game.py', current_game_mode],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return jsonify({"status": "Game started successfully", "mode": current_game_mode}), 200
        else:
            return jsonify({"status": "Game already running", "mode": current_game_mode}), 200
    except Exception as e:
        return jsonify({"status": "Error starting game", "error": str(e)}), 500


@game_bp.route('/stop-game', methods=['POST'])
@login_required
def stop_game():
    """Stop the gesture-based game system"""
    global game_process
    try:
        if game_process is not None:
            game_process.terminate()
            game_process = None
            return jsonify({"status": "Game stopped successfully"}), 200
        else:
            return jsonify({"status": "No game running"}), 200
    except Exception as e:
        return jsonify({"status": "Error stopping game", "error": str(e)}), 500


@game_bp.route('/get-game-mode', methods=['GET'])
@login_required
def get_game_mode():
    """Get current game mode"""
    return jsonify({"mode": current_game_mode}), 200
