from flask import Flask, render_template, Response, jsonify
import cv2
import time

# ✅ IMPORT CORRECT FUNCTIONS
from modules.voice.voice_control import start_voice, stop_voice, get_chat
from modules.gesture.gesture_mouse import (
    start_gesture,
    stop_gesture,
    get_gesture,
    get_frame   # 🔥 IMPORTANT FIX
)

app = Flask(__name__)


# =========================
# 🎥 VIDEO STREAM (FIXED)
# =========================
def generate_frames():
    while True:
        frame = get_frame()   # 🔥 GET FRAME FROM MODULE

        if frame is None:
            time.sleep(0.01)   # prevent CPU overload
            continue

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# =========================
# 📄 PAGES
# =========================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/gesture')
def gesture_page():
    return render_template('gesture.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/voice')
def voice():
    return render_template('voice.html')


# =========================
# ✋ GESTURE ROUTES
# =========================
@app.route('/start-gesture')
def start_gesture_route():
    start_gesture()
    return "Gesture Started"

@app.route('/stop-gesture')
def stop_gesture_route():
    stop_gesture()
    return "Gesture Stopped"

@app.route('/get-gesture')
def get_gesture_route():
    return jsonify({"gesture": get_gesture()})


# =========================
# 🎤 VOICE ROUTES
# =========================
@app.route('/start-voice')
def start_voice_route():
    start_voice()
    return "Voice Started"

@app.route('/stop-voice')
def stop_voice_route():
    stop_voice()
    return "Voice Stopped"

@app.route('/get-chat')
def chat():
    return jsonify({"chat": get_chat()})
# =========================
# 🚀 RUN
# =========================

if __name__ == "__main__":  # 🔥 ADD THIS
    app.run(debug=True, use_reloader=False)    