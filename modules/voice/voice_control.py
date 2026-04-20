import speech_recognition as sr
import pyautogui
import os
import threading
import pyttsx3
import queue

# =========================
# 🔊 TEXT TO SPEECH SETUP
# =========================
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)

speech_queue = queue.Queue()

# ✅ SINGLE SAFE WORKER
def speech_worker():
    while True:
        item = speech_queue.get()

        if item is None:
            break

        text, emotion = item

        try:
            # 🎭 Emotion control
            if emotion == "happy":
                engine.setProperty('rate', 180)
                engine.setProperty('volume', 1.0)

            elif emotion == "sad":
                engine.setProperty('rate', 130)
                engine.setProperty('volume', 0.6)

            elif emotion == "angry":
                engine.setProperty('rate', 200)
                engine.setProperty('volume', 1.0)

            elif emotion == "calm":
                engine.setProperty('rate', 150)
                engine.setProperty('volume', 0.8)

            else:
                engine.setProperty('rate', 170)
                engine.setProperty('volume', 1.0)

            engine.say(text)
            engine.runAndWait()

        except Exception as e:
            print("Speech Error:", e)

        speech_queue.task_done()


# 🔥 START ONLY ONE THREAD
threading.Thread(target=speech_worker, daemon=True).start()


def speak(text, emotion="normal"):
    speech_queue.put((text, emotion))


# =========================
# 🎤 SPEECH RECOGNITION
# =========================
recognizer = sr.Recognizer()

running = False
chat_history = []


# =========================
# 🔊 VOICE LOOP
# =========================
def voice_loop():
    global running, chat_history

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Voice system ready...")

        while running:
            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                command = recognizer.recognize_google(audio).lower()
                print("You said:", command)

                chat_history.append({"type": "user", "text": command})

                response = "Command not recognized"
                emotion = "normal"

                # 🎯 COMMANDS
                if "open browser" in command:
                    os.system("start chrome")
                    response = "Opening browser"
                    emotion = "happy"

                elif "left" in command:
                    pyautogui.press("left")
                    response = "Moving left"
                    emotion = "calm"

                elif "right" in command:
                    pyautogui.press("right")
                    response = "Moving right"
                    emotion = "calm"

                elif "scroll down" in command:
                    pyautogui.scroll(-500)
                    response = "Scrolling down"
                    emotion = "calm"

                elif "scroll up" in command:
                    pyautogui.scroll(500)
                    response = "Scrolling up"
                    emotion = "calm"

                elif "close" in command:
                    pyautogui.hotkey("alt", "f4")
                    response = "Closing window"
                    emotion = "angry"

                elif "shutdown" in command:
                    response = "Shutdown disabled for safety"
                    emotion = "sad"

                elif "volume up" in command:
                    pyautogui.press("volumeup")
                    response = "Increasing volume"

                elif "volume down" in command:
                    pyautogui.press("volumedown")
                    response = "Decreasing volume"

                elif "mute" in command:
                    pyautogui.press("volumemute")
                    response = "Muting sound"

                elif "screenshot" in command:
                    pyautogui.screenshot("screenshot.png")
                    response = "Screenshot taken"
                    emotion = "happy"

                elif "open notepad" in command:
                    os.system("notepad")
                    response = "Opening Notepad"

                elif "open calculator" in command:
                    os.system("calc")
                    response = "Opening Calculator"

                elif "open youtube" in command:
                    os.system("start https://youtube.com")
                    response = "Opening YouTube"

                elif "open google" in command:
                    os.system("start https://google.com")
                    response = "Opening Google"

                elif "stop listening" in command:
                    response = "Stopping voice system"
                    emotion = "sad"
                    running = False

                # 🤖 RESPONSE
                chat_history.append({"type": "bot", "text": response})

                speak(response, emotion)

            except sr.UnknownValueError:
                msg = "Could not understand"
                chat_history.append({"type": "bot", "text": msg})
                speak(msg, "sad")

            except sr.WaitTimeoutError:
                msg = "Listening timeout"
                chat_history.append({"type": "bot", "text": msg})
                speak(msg, "calm")

            except Exception as e:
                msg = f"Error: {str(e)}"
                chat_history.append({"type": "bot", "text": msg})
                speak("An error occurred", "sad")


# =========================
# ▶ START VOICE
# =========================
def start_voice():
    global running
    if not running:
        running = True
        threading.Thread(target=voice_loop, daemon=True).start()
        print("✅ Voice Started")
        speak("Voice system started", "happy")


# =========================
# 🛑 STOP VOICE
# =========================
def stop_voice():
    global running
    running = False
    print("🛑 Voice Stopped")
    speak("Voice system stopped", "sad")


# =========================
# 📡 CHAT HISTORY
# =========================
def get_chat():
    return chat_history[-20:]