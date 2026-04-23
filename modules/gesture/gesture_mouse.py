"""
🖱️ GESTURE MOUSE CONTROL SYSTEM
================================
Detect hand gestures via webcam and control mouse cursor.

GESTURES SUPPORTED:
- OPEN HAND: Move cursor smoothly with palm
- FIST (Index + Middle fingers up): Left Click
- THREE FINGERS UP: Right Click  
- THUMBS UP: Double Click
- SWIPE LEFT: Scroll Left
- SWIPE RIGHT: Scroll Right
- SWIPE UP: Scroll Up
- SWIPE DOWN: Scroll Down

INSTRUCTIONS:
1. Sit in front of camera ~50cm away
2. Show hand within the blue ROI box
3. Keep gestures clear and distinct
4. Hand detection range: 100-400 pixels from camera
"""

import cv2
import numpy as np
import pyautogui
import math
import time
import threading

cap = None  # Initialize as None, will be created when starting

screen_w, screen_h = pyautogui.size()

frame_global = None
gesture_text = "None"

prev_x, prev_y = 0, 0
last_click_time = 0
last_gesture = "NONE"
gesture_cooldown = 1.0  # Increased to 1 second to prevent accidental clicks

running = False  # 🔴 control flag
gesture_thread = None  # 🔴 thread reference


def get_frame():
    return frame_global


def get_gesture():
    return gesture_text


def start_system():
    global running
    running = True


def stop_system():
    global running
    running = False


def get_status():
    return "RUNNING" if running else "STOPPED"


def start_gesture():
    """✨ START GESTURE - Spawn background thread"""
    global gesture_thread, running, cap
    if gesture_thread is None or not gesture_thread.is_alive():
        # Initialize camera
        if cap is None or not cap.isOpened():
            cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cap.set(cv2.CAP_PROP_FPS, 30)
            time.sleep(1)  # Give camera time to initialize
        
        running = True
        gesture_thread = threading.Thread(target=gesture_loop, daemon=True)
        gesture_thread.start()
        print("✅ Gesture System Started")


def stop_gesture():
    """🛑 STOP GESTURE - Stop background thread"""
    global running, gesture_thread, cap
    running = False
    if gesture_thread and gesture_thread.is_alive():
        gesture_thread.join(timeout=2)  # Wait max 2 seconds
    gesture_thread = None
    
    # Release camera
    if cap is not None:
        cap.release()
        cap = None
    
    print("🛑 Gesture System Stopped")


def count_fingers(defects, cnt):
    """Count extended fingers from defects"""
    if defects is None:
        return 0
    
    defect_count = 0
    for i in range(len(defects)):
        s, e, f, d = defects[i][0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        
        a = math.dist(start, end)
        b = math.dist(start, far)
        c = math.dist(end, far)
        
        angle = math.degrees(math.acos((b**2 + c**2 - a**2) / (2*b*c + 0.0001)))
        
        if angle < 90:
            defect_count += 1
    
    return defect_count


def detect_swipe(cx, cy, prev_cx, prev_cy):
    """Detect swipe direction"""
    dx = cx - prev_cx
    dy = cy - prev_cy
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance < 20:  # Minimum swipe distance
        return "NONE"
    
    angle = math.degrees(math.atan2(dy, dx))
    
    if -45 <= angle <= 45:
        return "RIGHT"
    elif 45 < angle <= 135:
        return "DOWN"
    elif -135 <= angle < -45:
        return "UP"
    else:
        return "LEFT"


def gesture_loop():
    global frame_global, gesture_text, prev_x, prev_y, last_click_time, running, last_gesture, cap
    
    prev_cx, prev_cy = 0, 0
    gesture_time = time.time()
    gesture_confidence = 0
    gesture_stable_count = 0  # Track gesture stability
    last_detected_gesture = "NONE"

    while True:

        if not running:
            time.sleep(0.1)
            continue

        # Check if camera is available
        if cap is None or not cap.isOpened():
            frame_global = None
            gesture_text = "Camera not available"
            time.sleep(0.1)
            continue

        ret, frame = cap.read()
        if not ret:
            gesture_text = "Failed to read camera"
            time.sleep(0.1)
            continue

        frame = cv2.flip(frame, 1)

        # ROI (Region of Interest)
        roi = frame[100:400, 100:400]
        cv2.rectangle(frame, (100, 100), (400, 400), (0, 255, 0), 3)
        cv2.putText(frame, "ROI: Show hand here", (110, 90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # Skin detection - adjusted for better detection
        lower_skin = np.array([0, 20, 70])
        upper_skin = np.array([20, 255, 255])

        mask = cv2.inRange(hsv, lower_skin, upper_skin)

        kernel = np.ones((7, 7), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.GaussianBlur(mask, (9, 9), 100)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        gesture_text = "No Hand Detected"
        gesture_confidence = 0

        if contours:
            cnt = max(contours, key=lambda x: cv2.contourArea(x))
            contour_area = cv2.contourArea(cnt)

            if contour_area > 3000:  # Minimum hand size
                gesture_confidence = min(100, int((contour_area / 5000) * 100))

                x, y, w, h = cv2.boundingRect(cnt)
                cx = x + w // 2
                cy = y + h // 2

                # ✅ FIXED: Correct cursor mapping (not inverted)
                screen_x = np.interp(cx, [0, 300], [0, screen_w])  # Left hand = left screen
                screen_y = np.interp(cy, [0, 300], [0, screen_h])  # Top hand = top screen

                # ✅ FIXED: Reduced smoothing for more responsive control
                smooth_factor = 0.3  # Lower = more responsive (was 0.7)
                smooth_x = prev_x + (screen_x - prev_x) * smooth_factor
                smooth_y = prev_y + (screen_y - prev_y) * smooth_factor

                pyautogui.moveTo(int(smooth_x), int(smooth_y), duration=0.01)
                prev_x, prev_y = smooth_x, smooth_y

                # Convex hull and defects
                hull = cv2.convexHull(cnt, returnPoints=False)
                defect_count = 0

                if hull is not None and len(hull) > 3:
                    defects = cv2.convexityDefects(cnt, hull)
                    defect_count = count_fingers(defects, cnt)

                # ✅ FIXED: Correct gesture detection logic
                current_time = time.time()
                detected_gesture = "NONE"

                if defect_count == 0:
                    detected_gesture = "FIST"
                    gesture_text = f"✊ FIST - Left Click (Confidence: {gesture_confidence}%)"
                    
                elif defect_count == 1:
                    detected_gesture = "TWO_FINGERS"
                    gesture_text = f"✌️ TWO FINGERS - Right Click (Confidence: {gesture_confidence}%)"
                    
                elif defect_count == 2:
                    detected_gesture = "THREE_FINGERS"
                    gesture_text = f"🤟 THREE FINGERS - Double Click (Confidence: {gesture_confidence}%)"

                elif defect_count >= 3:
                    detected_gesture = "OPEN_HAND"
                    # Detect swipe
                    swipe = detect_swipe(cx, cy, prev_cx, prev_cy)
                    
                    if swipe == "LEFT":
                        detected_gesture = "SWIPE_LEFT"
                        gesture_text = f"← SWIPE LEFT (Confidence: {gesture_confidence}%)"
                    elif swipe == "RIGHT":
                        detected_gesture = "SWIPE_RIGHT"
                        gesture_text = f"→ SWIPE RIGHT (Confidence: {gesture_confidence}%)"
                    elif swipe == "UP":
                        detected_gesture = "SWIPE_UP"
                        gesture_text = f"↑ SWIPE UP (Confidence: {gesture_confidence}%)"
                    elif swipe == "DOWN":
                        detected_gesture = "SWIPE_DOWN"
                        gesture_text = f"↓ SWIPE DOWN (Confidence: {gesture_confidence}%)"
                    else:
                        gesture_text = f"👋 OPEN HAND - Move Cursor (Confidence: {gesture_confidence}%)"

                    prev_cx, prev_cy = cx, cy

                # ✅ FIXED: Gesture stability check (must detect same gesture 3 times)
                if detected_gesture == last_detected_gesture:
                    gesture_stable_count += 1
                else:
                    gesture_stable_count = 0
                    last_detected_gesture = detected_gesture

                # Only trigger action if gesture is stable and cooldown passed
                if gesture_stable_count >= 3 and current_time - gesture_time > gesture_cooldown:
                    if detected_gesture == "FIST":
                        pyautogui.click()
                        gesture_time = current_time
                        last_gesture = "CLICK"
                        gesture_stable_count = 0
                        
                    elif detected_gesture == "TWO_FINGERS":
                        pyautogui.click(button='right')
                        gesture_time = current_time
                        last_gesture = "RIGHT_CLICK"
                        gesture_stable_count = 0
                        
                    elif detected_gesture == "THREE_FINGERS":
                        pyautogui.click(clicks=2)
                        gesture_time = current_time
                        last_gesture = "DOUBLE_CLICK"
                        gesture_stable_count = 0
                        
                    elif detected_gesture == "SWIPE_LEFT":
                        pyautogui.scroll(5)
                        gesture_time = current_time
                        last_gesture = "SWIPE_LEFT"
                        gesture_stable_count = 0
                        
                    elif detected_gesture == "SWIPE_RIGHT":
                        pyautogui.scroll(-5)
                        gesture_time = current_time
                        last_gesture = "SWIPE_RIGHT"
                        gesture_stable_count = 0
                        
                    elif detected_gesture == "SWIPE_UP":
                        pyautogui.press('up')
                        gesture_time = current_time
                        last_gesture = "SWIPE_UP"
                        gesture_stable_count = 0
                        
                    elif detected_gesture == "SWIPE_DOWN":
                        pyautogui.press('down')
                        gesture_time = current_time
                        last_gesture = "SWIPE_DOWN"
                        gesture_stable_count = 0

                cv2.rectangle(roi, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.circle(roi, (cx, cy), 5, (0, 0, 255), -1)
                
                # Draw confidence bar
                bar_width = int((gesture_confidence / 100) * 80)
                cv2.rectangle(roi, (10, 260), (90, 280), (100, 100, 100), -1)
                cv2.rectangle(roi, (10, 260), (10 + bar_width, 280), (0, 255, 0), -1)
                cv2.putText(roi, f"Conf: {gesture_confidence}%", (10, 295),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
                
                # Show stability indicator
                stability_text = f"Stability: {gesture_stable_count}/3"
                cv2.putText(roi, stability_text, (10, 250),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)

        # Display info on frame
        cv2.putText(frame, f"Gesture: {gesture_text}", (10, 450),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, f"Cursor: ({int(prev_x)}, {int(prev_y)})", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        frame_global = frame


if __name__ == "__main__":
    start_gesture()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_gesture()
        cap.release()
        print("Gesture system closed")