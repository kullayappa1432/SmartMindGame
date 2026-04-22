"""
🎥 SIMPLE CAMERA TEST
=====================
Quick test to see if camera works with your exact configuration.
Press 'q' to quit.
"""

import cv2
import time

print("=" * 60)
print("🎥 SIMPLE CAMERA TEST")
print("=" * 60)

# Try Method 1: DirectShow (Windows)
print("\n[1] Trying DirectShow backend...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("   ❌ DirectShow failed")
    print("\n[2] Trying default backend...")
    cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("   ❌ Default backend failed")
    print("\n[3] Trying alternative camera indices...")
    
    for i in range(1, 4):
        print(f"   Trying index {i}...")
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            print(f"   ✅ Found camera at index {i}!")
            break
        cap.release()

if not cap.isOpened():
    print("\n❌ FAILED: No camera found!")
    print("\n🔧 NEXT STEPS:")
    print("   1. Close ALL apps that might use camera (Zoom, Teams, etc.)")
    print("   2. Check: Settings > Privacy > Camera > Allow apps to access camera")
    print("   3. Try opening Windows Camera app to verify camera works")
    print("   4. Restart your computer")
    print("   5. Run: python camera_diagnostic.py for detailed testing")
    exit(1)

print("\n✅ Camera opened successfully!")

# Set properties
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

print("⏳ Warming up camera (2 seconds)...")
time.sleep(2)

# Test read
ret, frame = cap.read()
if not ret:
    print("❌ ERROR: Cannot read frames from camera")
    print("   Camera is likely being used by another application")
    cap.release()
    exit(1)

print(f"✅ Frame captured! Resolution: {frame.shape[1]}x{frame.shape[0]}")
print("\n📹 Opening camera window...")
print("   Press 'q' to quit")
print("   If you see yourself, the camera is working! ✅")

frame_count = 0
start_time = time.time()

try:
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print(f"\n❌ Lost camera connection at frame {frame_count}")
            break
        
        # Flip for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Calculate FPS
        frame_count += 1
        elapsed = time.time() - start_time
        fps = frame_count / elapsed if elapsed > 0 else 0
        
        # Add info overlay
        cv2.putText(frame, "Camera Test - Press 'q' to quit", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        cv2.putText(frame, f"Frame: {frame_count}", (10, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Show frame
        cv2.imshow('Camera Test', frame)
        
        # Check for 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\n✅ User quit - test successful!")
            break

except KeyboardInterrupt:
    print("\n⚠️ Interrupted by user")

except Exception as e:
    print(f"\n❌ Error: {e}")

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("\n✅ Camera released")
    print(f"📊 Total frames captured: {frame_count}")
    print(f"⏱️ Average FPS: {fps:.1f}")
    
    if frame_count > 10:
        print("\n🎉 SUCCESS! Your camera is working perfectly!")
        print("   If it works here but not in your app:")
        print("   1. Make sure to stop this test before running the app")
        print("   2. Wait 5 seconds between stopping and starting")
        print("   3. Check if Flask app shows any error messages")
    else:
        print("\n⚠️ Camera worked but stopped quickly")
        print("   This might indicate an intermittent issue")

print("\n" + "=" * 60)
