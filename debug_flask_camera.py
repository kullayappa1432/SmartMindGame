"""
🔍 DEBUG FLASK CAMERA ISSUE
===========================
This will help identify why camera works in test but not in Flask app.
"""

import cv2
import time
import sys

print("=" * 60)
print("🔍 DEBUGGING FLASK CAMERA ISSUE")
print("=" * 60)

# Simulate Flask app camera initialization
print("\n[TEST 1] Simulating Flask app camera initialization...")

# First, let's see if camera is available
print("   Checking if camera is available...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("   ❌ Camera not available with DirectShow")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("   ❌ Camera not available with default backend")
        print("\n⚠️ ISSUE: Camera is locked by another process")
        print("   Did you close the test_camera_simple.py window?")
        print("   Wait 10 seconds and try again.")
        sys.exit(1)

print("   ✅ Camera opened")

# Set properties like Flask app does
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

print("   ⏳ Warming up (2 seconds)...")
time.sleep(2)

# Test frame read
ret, frame = cap.read()
if not ret:
    print("   ❌ Cannot read frames")
    cap.release()
    sys.exit(1)

print(f"   ✅ Frame read successful: {frame.shape[1]}x{frame.shape[0]}")

# Now test continuous reading like Flask does
print("\n[TEST 2] Testing continuous frame reading (like Flask video_feed)...")
success_count = 0
fail_count = 0

for i in range(30):  # Test 30 frames (~1 second)
    ret, frame = cap.read()
    if ret:
        success_count += 1
    else:
        fail_count += 1
        print(f"   ❌ Frame {i+1} failed")
    time.sleep(0.033)  # ~30 FPS

print(f"   📊 Success: {success_count}/30, Failed: {fail_count}/30")

if fail_count > 0:
    print("   ⚠️ ISSUE: Intermittent frame reading failures")
else:
    print("   ✅ All frames read successfully")

# Test with threading (like Flask app does)
print("\n[TEST 3] Testing with threading (like Flask app)...")

import threading

frame_global = None
running = True

def capture_loop():
    global frame_global, running
    while running:
        ret, frame = cap.read()
        if ret:
            frame_global = cv2.flip(frame, 1)
        time.sleep(0.033)

thread = threading.Thread(target=capture_loop, daemon=True)
thread.start()

time.sleep(2)  # Let it run for 2 seconds

if frame_global is not None:
    print("   ✅ Threading works - frames captured")
else:
    print("   ❌ Threading failed - no frames captured")

running = False
thread.join(timeout=1)

# Test JPEG encoding (like Flask does)
print("\n[TEST 4] Testing JPEG encoding (like Flask video_feed)...")
ret, frame = cap.read()
if ret:
    try:
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        print(f"   ✅ JPEG encoding works - {len(frame_bytes)} bytes")
    except Exception as e:
        print(f"   ❌ JPEG encoding failed: {e}")
else:
    print("   ❌ Cannot read frame for encoding")

# Cleanup
cap.release()

print("\n" + "=" * 60)
print("✅ DEBUG COMPLETE")
print("=" * 60)

print("\n📋 DIAGNOSIS:")
print("   If all tests passed, the issue is likely:")
print("   1. Flask app not releasing camera properly on previous run")
print("   2. Browser caching old video feed")
print("   3. Route timing issue")
print("\n🔧 SOLUTIONS TO TRY:")
print("   1. Restart Flask app completely (Ctrl+C, wait 5 sec, restart)")
print("   2. Clear browser cache (Ctrl+Shift+Delete)")
print("   3. Try different browser")
print("   4. Check Flask terminal for error messages")
print("   5. Use the fixed version: python app_fixed.py")
