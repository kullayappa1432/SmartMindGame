
from flask import Blueprint, jsonify, request
from flask_login import login_required
import subprocess
import os
import sys
import time

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
            # Get the absolute path to the game script
            app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            script_path = os.path.join(app_dir, 'modules', 'gesture', 'gesture_game.py')
            
            # Check if file exists
            if not os.path.exists(script_path):
                return jsonify({
                    "status": "Error starting game",
                    "error": f"Game script not found at {script_path}"
                }), 500
            
            # Try to start game with mode parameter
            try:
                game_process = subprocess.Popen(
                    [sys.executable, script_path, current_game_mode],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=app_dir
                )
                # Give it a moment to start
                time.sleep(0.5)
                
                # Check if process is still running
                poll_result = game_process.poll()
                if poll_result is not None:
                    # Process exited, get error
                    stderr = game_process.stderr.read().decode('utf-8', errors='ignore')
                    stdout = game_process.stdout.read().decode('utf-8', errors='ignore')
                    error_msg = stderr or stdout or f"Process exited with code {poll_result}"
                    game_process = None
                    return jsonify({
                        "status": "Error starting game",
                        "error": error_msg
                    }), 500
                
                return jsonify({"status": "Game started successfully", "mode": current_game_mode}), 200
            except Exception as e:
                game_process = None
                return jsonify({"status": "Error starting game", "error": str(e)}), 500
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
