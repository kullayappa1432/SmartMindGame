import cv2
import numpy as np
import pyautogui
import math
import time

cap = cv2.VideoCapture(0)

screen_w, screen_h = pyautogui.size()

frame_global = None
gesture_text = "None"

prev_x, prev_y = 0, 0
last_click_time = 0

running = False  # 🔴 control flag


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


def gesture_loop():
    global frame_global, gesture_text, prev_x, prev_y, last_click_time, running

    while True:

        if not running:
            time.sleep(0.1)
            continue

        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)

        # ROI
        roi = frame[100:400, 100:400]
        cv2.rectangle(frame, (100, 100), (400, 400), (255, 0, 0), 2)

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        lower_skin = np.array([0, 40, 60])
        upper_skin = np.array([25, 255, 255])

        mask = cv2.inRange(hsv, lower_skin, upper_skin)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)
        mask = cv2.GaussianBlur(mask, (5, 5), 100)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        gesture_text = "No Hand"

        if contours:
            cnt = max(contours, key=lambda x: cv2.contourArea(x))

            if cv2.contourArea(cnt) > 4000:

                x, y, w, h = cv2.boundingRect(cnt)
                cx = x + w // 2
                cy = y + h // 2

                # Cursor mapping
                screen_x = np.interp(cx, [0, 300], [screen_w, 0])
                screen_y = np.interp(cy, [0, 300], [0, screen_h])

                smooth_x = prev_x + (screen_x - prev_x) / 4
                smooth_y = prev_y + (screen_y - prev_y) / 4

                pyautogui.moveTo(smooth_x, smooth_y)
                prev_x, prev_y = smooth_x, smooth_y

                # Convex hull
                hull = cv2.convexHull(cnt, returnPoints=False)

                defect_count = 0

                if hull is not None and len(hull) > 3:
                    defects = cv2.convexityDefects(cnt, hull)

                    if defects is not None:
                        for i in range(defects.shape[0]):
                            s, e, f, d = defects[i][0]

                            start = tuple(cnt[s][0])
                            end = tuple(cnt[e][0])
                            far = tuple(cnt[f][0])

                            a = math.dist(start, end)
                            b = math.dist(start, far)
                            c = math.dist(end, far)

                            angle = math.degrees(
                                math.acos((b**2 + c**2 - a**2) / (2*b*c))
                            )

                            if angle < 90:
                                defect_count += 1

                # Gesture logic
                if defect_count <= 1:
                    gesture_text = "FIST (CLICK)"

                    if time.time() - last_click_time > 1:
                        pyautogui.click()
                        last_click_time = time.time()

                elif defect_count >= 3:
                    gesture_text = "OPEN HAND"

                else:
                    gesture_text = "UNKNOWN"

                cv2.rectangle(roi, (x, y), (x+w, y+h), (0,255,0), 2)

        cv2.putText(frame, f"Gesture: {gesture_text}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        frame_global = frame
   