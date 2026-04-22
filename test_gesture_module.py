"""
🧪 TEST GESTURE MODULE DIRECTLY
================================
This tests the gesture module without Flask to isolate the issue.
"""

import sys
import time

print("=" * 60)
print("🧪 TESTING GESTURE MODULE DIRECTLY")
print("=" * 60)

# Import the gesture module
print("\n[1] Importing gesture module...")
try:
    from modules.gesture.gesture_mouse_mediapipe import start_gesture, stop_gesture, get_frame, get_gesture
    print("   ✅ Import successful")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Start gesture system
print("\n[2] Starting gesture system...")
success = start_gesture()

if not success:
    print("   ❌ Failed to start gesture system")
    print("\n🔧 TROUBLESHOOTING:")
    print("   1. Make sure test_camera_simple.py is closed")
    print("   2. Wait 10 seconds and try again")
    print("   3. Restart your computer")
    sys.exit(1)

print("   ✅ Gesture system started")

# Wait for initialization
print("\n[3] Waiting for camera to initialize (3 seconds)...")
time.sleep(3)

# Test frame retrieval
print("\n[4] Testing frame retrieval...")
frame_count = 0
none_count = 0

for i in range(30):
    frame = get_frame()
    if frame is not None:
        frame_count += 1
        if i == 0:
            print(f"   ✅ First frame received! Shape: {frame.shape}")
    else:
        none_count += 1
        if i < 5:
            print(f"   ⚠️ Frame {i+1} is None")
    time.sleep(0.1)

print(f"\n   📊 Results: {frame_count}/30 frames received, {none_count}/30 were None")

if frame_count == 0:
    print("\n   ❌ ISSUE: No frames received!")
    print("   The gesture module started but isn't capturing frames.")
    print("\n   Possible causes:")
    print("   1. Camera opened but can't read frames (another app using it)")
    print("   2. Threading issue in gesture_loop")
    print("   3. Camera initialization succeeded but frame reading failed")
elif none_count > 0:
    print(f"\n   ⚠️ WARNING: {none_count} frames were None")
    print("   Camera is working but has intermittent issues")
else:
    print("\n   ✅ SUCCESS: All frames received!")

# Test gesture detection
print("\n[5] Testing gesture detection...")
for i in range(5):
    gesture = get_gesture()
    print(f"   Gesture {i+1}: {gesture}")
    time.sleep(0.5)

# Display frames (optional)
print("\n[6] Opening display window (press 'q' to quit)...")
print("   If you see yourself, the module is working correctly!")

import cv2

try:
    for i in range(100):
        frame = get_frame()
        
        if frame is not None:
            cv2.imshow('Gesture Module Test', frame)
            
            if cv2.waitKey(100) & 0xFF == ord('q'):
                print("   User pressed 'q'")
                break
        else:
            print(f"   ⚠️ Frame {i+1} is None")
            time.sleep(0.1)
    
    cv2.destroyAllWindows()
    print("   ✅ Display test complete")
    
except Exception as e:
    print(f"   ⚠️ Display error: {e}")

# Stop gesture system
print("\n[7] Stopping gesture system...")
stop_gesture()
print("   ✅ Gesture system stopped")

print("\n" + "=" * 60)
print("✅ TEST COMPLETE")
print("=" * 60)

print("\n📋 SUMMARY:")
if frame_count > 25:
    print("   ✅ Gesture module works perfectly!")
    print("\n   If it works here but not in Flask:")
    print("   1. Flask might not be waiting long enough for initialization")
    print("   2. Browser might be caching old video feed")
    print("   3. Flask route timing issue")
    print("\n   SOLUTION: Use the updated app.py with better error handling")
elif frame_count > 0:
    print("   ⚠️ Gesture module works but has issues")
    print("   Camera is intermittently failing")
else:
    print("   ❌ Gesture module not working")
    print("   Camera opens but can't read frames")
    print("   Another application might be using the camera")
