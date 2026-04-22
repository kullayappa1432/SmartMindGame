"""
🖱️ MEDIAPIPE GESTURE MOUSE CONTROL SYSTEM
==========================================
Professional hand tracking using Google MediaPipe for accurate gesture recognition.

GESTURES SUPPORTED:
- INDEX FINGER UP: Move cursor (only index finger extended)
- FIST (all fingers closed): Left Click
- PEACE SIGN (index + middle up): Right Click
- THREE FINGERS (index + middle + ring): Double Click
- PINCH (thumb + index touching): Drag/Hold
- PALM OPEN (all 5 fingers up): Scroll Mode

HAND LANDMARKS (21 points):
0: WRIST
1-4: THUMB (CMC, MCP, IP, TIP)
5-8: INDEX (MCP, PIP, DIP, TIP)
9-12: MIDDLE (MCP, PIP, DIP, TIP)
13-16: RING (MCP, PIP, DIP, TIP)
17-20: PINKY (MCP, PIP, DIP, TIP)
"""

import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time
import threading
import math

# ===========================
# MEDIAPIPE INITIALIZATION
# ===========================
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Hand detector with optimized settings
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ===========================
# GLOBAL VARIABLES
# ===========================
cap = None
screen_w, screen_h = pyautogui.size()

frame_global = None
gesture_text = "No Hand Detected"
hand_landmarks_global = None

# Cursor smoothing
prev_x, prev_y = screen_w // 2, screen_h // 2
smooth_factor = 0.5  # 0.1 = very responsive, 0.9 = very smooth

# Gesture control
running = False
gesture_thread = None
last_gesture = "NONE"
gesture_time = time.time()
gesture_cooldown = 0.8  # Seconds between actions
gesture_stable_count = 0
last_detected_gesture = "NONE"
stability_threshold = 3  # Frames to confirm gesture

# Drag mode
drag_active = False

# ===========================
# CONFIGURATION (ADJUST HERE)
# ===========================
CONFIG = {
    # Cursor control
    'smooth_factor': 0.5,           # 0.1-0.9 (lower = more responsive)
    'cursor_speed': 1.5,            # Multiplier for cursor movement
    
    # Gesture detection
    'gesture_cooldown': 0.8,        # Seconds between actions
    'stability_threshold': 3,       # Frames to confirm gesture
    
    # Finger detection thresholds
    'finger_curl_threshold': 0.1,   # How much finger must curl to be "closed"
    'pinch_threshold': 0.05,        # Distance for pinch detection
    
    # Camera
    'camera_index': 0,              # 0 = default camera
    'frame_width': 640,
    'frame_height': 480,
    'fps': 30,
}


# ===========================
# UTILITY FUNCTIONS
# ===========================
def get_frame():
    """Return current frame for video streaming"""
    return frame_global


def get_gesture():
    """Return current gesture text"""
    return gesture_text


def get_status():
    """Return system status"""
    return "RUNNING" if running else "STOPPED"


def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points"""
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def is_finger_extended(landmarks, finger_tip_id, finger_pip_id, finger_mcp_id):
    """
    Check if a finger is extended by comparing tip position to joints
    
    Args:
        landmarks: Hand landmarks
        finger_tip_id: Landmark ID for finger tip
        finger_pip_id: Landmark ID for PIP joint
        finger_mcp_id: Landmark ID for MCP joint
    
    Returns:
        bool: True if finger is extended
    """
    tip = landmarks[finger_tip_id]
    pip = landmarks[finger_pip_id]
    mcp = landmarks[finger_mcp_id]
    
    # Finger is extended if tip is higher (lower y value) than PIP and MCP
    return tip.y < pip.y and tip.y < mcp.y


def is_thumb_extended(landmarks):
    """Check if thumb is extended (different logic than other fingers)"""
    thumb_tip = landmarks[4]
    thumb_ip = landmarks[3]
    thumb_mcp = landmarks[2]
    
    # Thumb is extended if tip is further from palm than IP joint
    return thumb_tip.x < thumb_ip.x  # For right hand


def count_extended_fingers(landmarks):
    """
    Count how many fingers are extended
    
    Returns:
        dict: {
            'count': int,
            'thumb': bool,
            'index': bool,
            'middle': bool,
            'ring': bool,
            'pinky': bool
        }
    """
    fingers = {
        'thumb': is_thumb_extended(landmarks),
        'index': is_finger_extended(landmarks, 8, 6, 5),
        'middle': is_finger_extended(landmarks, 12, 10, 9),
        'ring': is_finger_extended(landmarks, 16, 14, 13),
        'pinky': is_finger_extended(landmarks, 20, 18, 17),
    }
    
    fingers['count'] = sum(fingers.values())
    return fingers


def is_pinching(landmarks, frame_width, frame_height):
    """Check if thumb and index finger are pinching"""
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    
    # Convert normalized coordinates to pixel coordinates
    thumb_pos = (thumb_tip.x * frame_width, thumb_tip.y * frame_height)
    index_pos = (index_tip.x * frame_width, index_tip.y * frame_height)
    
    distance = calculate_distance(thumb_pos, index_pos)
    
    # Pinch detected if distance is small
    threshold = CONFIG['pinch_threshold'] * frame_width
    return distance < threshold


def detect_gesture(landmarks, frame_width, frame_height):
    """
    Detect gesture based on hand landmarks
    
    Returns:
        str: Gesture name
    """
    fingers = count_extended_fingers(landmarks)
    
    # GESTURE LOGIC (CONFIGURABLE)
    
    # FIST: All fingers closed
    if fingers['count'] == 0:
        return "FIST"
    
    # INDEX ONLY: Move cursor
    elif fingers['count'] == 1 and fingers['index']:
        return "CURSOR_MOVE"
    
    # PEACE SIGN: Index + Middle
    elif fingers['count'] == 2 and fingers['index'] and fingers['middle']:
        return "PEACE"
    
    # THREE FINGERS: Index + Middle + Ring
    elif fingers['count'] == 3 and fingers['index'] and fingers['middle'] and fingers['ring']:
        return "THREE_FINGERS"
    
    # FOUR FINGERS: All except thumb
    elif fingers['count'] == 4 and not fingers['thumb']:
        return "FOUR_FINGERS"
    
    # PALM OPEN: All 5 fingers
    elif fingers['count'] == 5:
        return "PALM_OPEN"
    
    # PINCH: Thumb and index touching
    elif is_pinching(landmarks, frame_width, frame_height):
        return "PINCH"
    
    # THUMB UP: Only thumb extended
    elif fingers['count'] == 1 and fingers['thumb']:
        return "THUMB_UP"
    
    else:
        return "UNKNOWN"


# ===========================
# SYSTEM CONTROL
# ===========================
def start_gesture():
    """Start gesture recognition system"""
    global gesture_thread, running, cap
    
    if gesture_thread is None or not gesture_thread.is_alive():
        # Release any existing camera connection
        if cap is not None:
            cap.release()
            time.sleep(0.5)
        
        # Try multiple camera initialization methods
        print("🎥 Attempting to open camera...")
        
        # Method 1: Try default camera with DirectShow (Windows)
        cap = cv2.VideoCapture(CONFIG['camera_index'], cv2.CAP_DSHOW)
        
        if not cap.isOpened():
            print("   Method 1 (DirectShow) failed, trying Method 2...")
            cap.release()
            # Method 2: Try without backend specification
            cap = cv2.VideoCapture(CONFIG['camera_index'])
        
        if not cap.isOpened():
            print("   Method 2 failed, trying alternative camera indices...")
            cap.release()
            # Method 3: Try other camera indices
            for i in range(1, 4):
                print(f"   Trying camera index {i}...")
                cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
                if cap.isOpened():
                    print(f"✅ Camera found at index {i}")
                    CONFIG['camera_index'] = i
                    break
                cap.release()
        
        # Final check
        if not cap.isOpened():
            print("❌ ERROR: Could not open camera on any index")
            print("🔧 TROUBLESHOOTING:")
            print("   1. Close any apps using the camera (Zoom, Teams, etc.)")
            print("   2. Check Windows Privacy Settings > Camera")
            print("   3. Run camera_diagnostic.py for detailed testing")
            cap = None
            return False
        
        # Configure camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CONFIG['frame_width'])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CONFIG['frame_height'])
        cap.set(cv2.CAP_PROP_FPS, CONFIG['fps'])
        
        # Give camera time to initialize and warm up
        print("⏳ Warming up camera...")
        time.sleep(2.0)
        
        # Test read a frame
        ret, test_frame = cap.read()
        if not ret:
            print("❌ ERROR: Camera opened but cannot read frames")
            print("   This usually means another app is using the camera")
            cap.release()
            cap = None
            return False
        
        print(f"✅ Camera initialized successfully! Resolution: {test_frame.shape[1]}x{test_frame.shape[0]}")
        
        # Start gesture thread
        running = True
        gesture_thread = threading.Thread(target=gesture_loop, daemon=True)
        gesture_thread.start()
        print("✅ MediaPipe Gesture System Started")
        return True
    
    return True


def stop_gesture():
    """Stop gesture recognition system"""
    global running, gesture_thread, cap, hands
    
    running = False
    
    if gesture_thread and gesture_thread.is_alive():
        gesture_thread.join(timeout=2)
    gesture_thread = None
    
    # Release camera
    if cap is not None:
        cap.release()
        cap = None
    
    print("🛑 MediaPipe Gesture System Stopped")


# ===========================
# MAIN GESTURE LOOP
# ===========================
def gesture_loop():
    """Main loop for gesture recognition"""
    global frame_global, gesture_text, prev_x, prev_y, running
    global last_gesture, gesture_time, gesture_stable_count, last_detected_gesture
    global drag_active, hand_landmarks_global
    
    print("🎥 Starting gesture loop...")
    loop_count = 0
    
    while True:
        if not running:
            time.sleep(0.1)
            continue
        
        # Check camera availability
        if cap is None or not cap.isOpened():
            if loop_count % 10 == 0:  # Print every 10 iterations to avoid spam
                print(f"⚠️ gesture_loop: Camera not available (iteration {loop_count})")
            frame_global = None
            gesture_text = "❌ Camera not available"
            time.sleep(0.5)
            loop_count += 1
            continue
        
        # Read frame
        ret, frame = cap.read()
        if not ret:
            if loop_count % 10 == 0:
                print(f"⚠️ gesture_loop: Failed to read frame (iteration {loop_count})")
            gesture_text = "❌ Failed to read camera"
            time.sleep(0.1)
            loop_count += 1
            continue
        
        # Log first successful frame
        if loop_count == 0:
            print(f"✅ gesture_loop: First frame captured! Shape: {frame.shape}")
        
        loop_count += 1
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame with MediaPipe
        results = hands.process(rgb_frame)
        
        # Default state
        gesture_text = "👋 Show your hand"
        current_gesture = "NONE"
        
        # If hand detected
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            hand_landmarks_global = hand_landmarks
            
            # Draw hand landmarks on frame
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
            
            # Get landmark list
            landmarks = hand_landmarks.landmark
            
            # Detect gesture
            current_gesture = detect_gesture(landmarks, frame_width, frame_height)
            
            # Get index finger tip position for cursor control
            index_tip = landmarks[8]
            cursor_x = int(index_tip.x * screen_w * CONFIG['cursor_speed'])
            cursor_y = int(index_tip.y * screen_h * CONFIG['cursor_speed'])
            
            # Clamp to screen bounds
            cursor_x = max(0, min(screen_w - 1, cursor_x))
            cursor_y = max(0, min(screen_h - 1, cursor_y))
            
            # Apply smoothing
            smooth_x = prev_x + (cursor_x - prev_x) * CONFIG['smooth_factor']
            smooth_y = prev_y + (cursor_y - prev_y) * CONFIG['smooth_factor']
            
            # Move cursor
            pyautogui.moveTo(int(smooth_x), int(smooth_y), duration=0)
            prev_x, prev_y = smooth_x, smooth_y
            
            # Gesture stability check
            if current_gesture == last_detected_gesture:
                gesture_stable_count += 1
            else:
                gesture_stable_count = 0
                last_detected_gesture = current_gesture
            
            # Execute gesture action if stable
            current_time = time.time()
            
            if gesture_stable_count >= CONFIG['stability_threshold']:
                if current_time - gesture_time > CONFIG['gesture_cooldown']:
                    
                    if current_gesture == "FIST":
                        gesture_text = "✊ FIST - Left Click"
                        pyautogui.click()
                        gesture_time = current_time
                        gesture_stable_count = 0
                    
                    elif current_gesture == "PEACE":
                        gesture_text = "✌️ PEACE - Right Click"
                        pyautogui.click(button='right')
                        gesture_time = current_time
                        gesture_stable_count = 0
                    
                    elif current_gesture == "THREE_FINGERS":
                        gesture_text = "🤟 THREE FINGERS - Double Click"
                        pyautogui.doubleClick()
                        gesture_time = current_time
                        gesture_stable_count = 0
                    
                    elif current_gesture == "PALM_OPEN":
                        gesture_text = "🖐️ PALM OPEN - Scroll Up"
                        pyautogui.scroll(3)
                        gesture_time = current_time
                    
                    elif current_gesture == "FOUR_FINGERS":
                        gesture_text = "🖖 FOUR FINGERS - Scroll Down"
                        pyautogui.scroll(-3)
                        gesture_time = current_time
                    
                    elif current_gesture == "PINCH":
                        if not drag_active:
                            gesture_text = "🤏 PINCH - Drag Start"
                            pyautogui.mouseDown()
                            drag_active = True
                        else:
                            gesture_text = "🤏 PINCH - Dragging..."
                    
                    elif current_gesture == "THUMB_UP":
                        gesture_text = "👍 THUMB UP - Volume Up"
                        pyautogui.press('volumeup')
                        gesture_time = current_time
                        gesture_stable_count = 0
                    
                    elif current_gesture == "CURSOR_MOVE":
                        gesture_text = "☝️ INDEX - Move Cursor"
                        if drag_active:
                            pyautogui.mouseUp()
                            drag_active = False
                    
                    else:
                        gesture_text = f"❓ {current_gesture}"
                else:
                    # Show cooldown
                    remaining = CONFIG['gesture_cooldown'] - (current_time - gesture_time)
                    gesture_text = f"⏳ Cooldown: {remaining:.1f}s"
            else:
                # Show stability progress
                gesture_text = f"🎯 {current_gesture} [{gesture_stable_count}/{CONFIG['stability_threshold']}]"
            
            # Release drag if hand lost
            if drag_active and current_gesture != "PINCH":
                pyautogui.mouseUp()
                drag_active = False
        
        else:
            # No hand detected
            hand_landmarks_global = None
            if drag_active:
                pyautogui.mouseUp()
                drag_active = False
        
        # Draw UI elements
        draw_ui(frame, gesture_text, prev_x, prev_y, gesture_stable_count)
        
        # Update global frame
        frame_global = frame


def draw_ui(frame, gesture_text, cursor_x, cursor_y, stability):
    """Draw UI elements on frame"""
    height, width, _ = frame.shape
    
    # Background overlay for text
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (width, 80), (0, 0, 0), -1)
    cv2.rectangle(overlay, (0, height - 60), (width, height), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    
    # Gesture text
    cv2.putText(frame, f"Gesture: {gesture_text}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Cursor position
    cv2.putText(frame, f"Cursor: ({int(cursor_x)}, {int(cursor_y)})", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    
    # Status
    status_text = "RUNNING" if running else "STOPPED"
    status_color = (0, 255, 0) if running else (0, 0, 255)
    cv2.putText(frame, f"Status: {status_text}", (10, height - 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
    
    # Stability bar
    bar_width = int((stability / CONFIG['stability_threshold']) * 200)
    cv2.rectangle(frame, (10, height - 15), (210, height - 5), (50, 50, 50), -1)
    cv2.rectangle(frame, (10, height - 15), (10 + bar_width, height - 5), (0, 255, 0), -1)
    
    # FPS counter
    cv2.putText(frame, f"MediaPipe Active", (width - 200, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)


# ===========================
# MAIN ENTRY POINT
# ===========================
if __name__ == "__main__":
    print("🚀 Starting MediaPipe Gesture Control...")
    start_gesture()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⚠️ Stopping...")
        stop_gesture()
        print("✅ Stopped")
