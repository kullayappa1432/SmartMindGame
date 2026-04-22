"""
🔍 CAMERA DIAGNOSTIC TOOL
=========================
This script will help identify why your camera isn't opening.
Run this to diagnose camera issues.
"""

import cv2
import sys
import time

print("=" * 60)
print("🔍 CAMERA DIAGNOSTIC TOOL")
print("=" * 60)

# Test 1: Check OpenCV installation
print("\n[TEST 1] Checking OpenCV installation...")
try:
    print(f"✅ OpenCV version: {cv2.__version__}")
except Exception as e:
    print(f"❌ OpenCV error: {e}")
    sys.exit(1)

# Test 2: Try to open default camera (index 0)
print("\n[TEST 2] Attempting to open camera index 0...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Failed to open camera index 0")
    print("\n[TEST 3] Trying alternative camera indices...")
    
    # Try other camera indices
    for i in range(1, 5):
        print(f"   Trying camera index {i}...")
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"✅ SUCCESS! Camera found at index {i}")
            break
        cap.release()
    
    if not cap.isOpened():
        print("\n❌ No camera found on any index (0-4)")
        print("\n🔧 TROUBLESHOOTING STEPS:")
        print("   1. Check if your camera is physically connected")
        print("   2. Check if another application is using the camera")
        print("   3. Try closing Zoom, Teams, Skype, or other video apps")
        print("   4. Check Windows Camera app to see if camera works there")
        print("   5. Update your camera drivers")
        print("   6. Check Windows Privacy Settings:")
        print("      Settings > Privacy > Camera > Allow apps to access camera")
        sys.exit(1)
else:
    print("✅ Camera opened successfully!")

# Test 3: Try to read a frame
print("\n[TEST 4] Attempting to read frame from camera...")
time.sleep(1)  # Give camera time to initialize

ret, frame = cap.read()

if not ret:
    print("❌ Failed to read frame from camera")
    print("\n🔧 POSSIBLE ISSUES:")
    print("   1. Camera is being used by another application")
    print("   2. Camera driver issue")
    print("   3. Insufficient permissions")
else:
    print(f"✅ Frame read successfully! Resolution: {frame.shape[1]}x{frame.shape[0]}")

# Test 4: Try to set camera properties
print("\n[TEST 5] Testing camera property configuration...")
try:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"✅ Camera properties set:")
    print(f"   Width: {actual_width}")
    print(f"   Height: {actual_height}")
    print(f"   FPS: {actual_fps}")
except Exception as e:
    print(f"⚠️ Warning: Could not set camera properties: {e}")

# Test 5: Try to capture multiple frames
print("\n[TEST 6] Testing continuous frame capture (5 frames)...")
success_count = 0
for i in range(5):
    ret, frame = cap.read()
    if ret:
        success_count += 1
        print(f"   Frame {i+1}: ✅")
    else:
        print(f"   Frame {i+1}: ❌")
    time.sleep(0.1)

print(f"\n📊 Successfully captured {success_count}/5 frames")

# Test 6: Display a test window (optional)
print("\n[TEST 7] Opening test window...")
print("   Press 'q' to close the window and complete the test")

try:
    for i in range(100):  # Show for ~10 seconds
        ret, frame = cap.read()
        if ret:
            # Flip frame for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Add text overlay
            cv2.putText(frame, "Camera Test - Press 'q' to quit", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Frame: {i+1}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            
            cv2.imshow('Camera Test', frame)
            
            # Break on 'q' key
            if cv2.waitKey(100) & 0xFF == ord('q'):
                print("   User pressed 'q' - closing window")
                break
        else:
            print(f"   ❌ Failed to read frame {i+1}")
            break
    
    cv2.destroyAllWindows()
    print("✅ Test window closed successfully")
    
except Exception as e:
    print(f"⚠️ Could not display test window: {e}")
    print("   This is normal if running in a non-GUI environment")

# Cleanup
cap.release()
print("\n" + "=" * 60)
print("✅ DIAGNOSTIC COMPLETE")
print("=" * 60)

print("\n📋 SUMMARY:")
print("   If all tests passed, your camera is working correctly.")
print("   If tests failed, follow the troubleshooting steps above.")
print("\n   If camera works here but not in the app, the issue is likely:")
print("   1. Camera already in use by another process")
print("   2. Threading issue in the application")
print("   3. Timing issue (camera needs more initialization time)")
