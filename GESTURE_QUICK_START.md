# Gesture Control - Quick Start Guide

## Installation

### Step 1: Install Required Packages
```bash
pip install opencv-python mediapipe pyautogui pygame numpy
```

### Step 2: Run the System

**For Mouse Control:**
```bash
python modules/gesture/gesture_mouse.py
```

**For Gaming:**
```bash
python modules/gesture/gesture_game.py
```

## Quick Guide

### Gesture Mouse Control
- **Open Hand** = Move cursor
- **Fist** = Left click
- **Peace Sign** = Right click  
- **Three Fingers** = Double click
- **Swipes** = Scroll actions

### Gesture Games
- **Menu**: Press 1-5 to select game
- **Play**: Use LEFT/RIGHT/UP gestures
- **Exit**: Press Q to return to menu

## Gestures Visualization

```
HAND REGION (Keep hand here):
┌──────────────────────────┐
│     ^ UP (Jump)          │
│    /|\                   │
│   / | \                  │
│ < CENTER > LEFT/RIGHT    │
│   \ | /                  │
│    \|/                   │
│     v DOWN               │
└──────────────────────────┘

HAND SHAPES:
✊ = Fist (Click)
✌️ = Two fingers (Right-click)
🤟 = Three fingers (Double-click)  
👋 = Open hand (Cursor/Move)
```

## System Requirements
- Webcam (30 FPS+)
- Python 3.7+
- Windows/Mac/Linux
- 4GB RAM minimum
- Good lighting

## Troubleshooting

### Camera not detected?
```bash
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

### Poor hand detection?
- Improve lighting
- Increase camera distance slightly
- Use plain background
- Show full hand in frame

### Game lags?
- Close background apps
- Reduce resolution
- Move camera closer
- Check CPU usage

## Pro Tips
1. Sit 50-60cm from camera
2. Use natural lighting (window light best)
3. Practice gestures slowly first
4. Make gestures clear and distinct
5. Keep hand within ROI box
6. Calibrate distance for your setup

For detailed documentation, see: `modules/gesture/README.md`
