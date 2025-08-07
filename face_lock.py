import sys

# Preload check block
if "--preload" in sys.argv:
    import cv2
    import numpy as np
    import mediapipe as mp
    import platform
    import subprocess
    import math
    import time
    sys.exit(0)

import os
import cv2
import mediapipe as mp
import numpy as np
import time
import platform
import subprocess
import math

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(min_detection_confidence=0.7, min_tracking_confidence=0.7)

NOSE_TIP_IDX = 1
EASY_PATTERN = ['right', 'left', 'right']
PATTERN_LENGTH = 3
PAUSE_SECONDS = 0.6
BACK_HOLD_SECONDS = 2
center_hold_start = None

def get_direction(p1, p2):
    dx = p2[0] - p1[0]
    if dx > 10:
        return 'right'
    elif dx < -10:
        return 'left'
    return 'still'

def lock_system():
    system = platform.system()
    if system == 'Windows':
        subprocess.run('rundll32.exe user32.dll,LockWorkStation', shell=True)
    elif system == 'Linux':
        subprocess.run(['gnome-screensaver-command', '--lock'])
    elif system == 'Darwin':
        subprocess.run(['/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession', '-suspend'])

def draw_centered_text(frame, text, y, font=cv2.FONT_HERSHEY_SIMPLEX, scale=1.0, color=(0, 255, 255), thickness=2):
    text_size = cv2.getTextSize(text, font, scale, thickness)[0]
    x = (frame.shape[1] - text_size[0]) // 2
    cv2.putText(frame, text, (x, y), font, scale, color, thickness, cv2.LINE_AA)

def draw_glowing_nose_point(frame, center, radius=12):
    overlay = frame.copy()
    glow_color = (255, 80, 20)
    cv2.circle(overlay, center, radius + 8, (glow_color[0], glow_color[1], glow_color[2]), -1)
    cv2.circle(overlay, center, radius, (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

def draw_pulsating_circle(frame, center, time_val, base_radius=50, color=(255, 0, 255)):
    pulse_radius = int(base_radius + 10 * math.sin(time_val * 2))
    overlay = frame.copy()
    cv2.circle(overlay, center, pulse_radius, color, 2)
    cv2.circle(overlay, center, pulse_radius + 5, (color[0], color[1], color[2], 100), 1)
    alpha = 0.4 + 0.2 * math.sin(time_val * 2)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

def run_face_pattern_lock():
    global center_hold_start
    cap = cv2.VideoCapture(0)
    trail = []
    direction_sequence = []
    last_gesture_time = time.time()
    unlocked = False
    show_message = False
    incorrect_attempt = False
    message_time = 0

    print("[INFO] Perform pattern ➡️ ⬅️ ➡️ using nose to lock the system...")
    print("[INFO] To go back, hold nose in center area of screen for 2 seconds.")

    start_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)
        h, w, _ = frame.shape
        center_x = w // 2
        center_y = h // 2

        elapsed = time.time() - start_time

        if results.multi_face_landmarks:
            face = results.multi_face_landmarks[0].landmark
            nose = face[NOSE_TIP_IDX]
            nose_point = (int(nose.x * w), int(nose.y * h))
            trail.append(nose_point)

            if len(trail) > 20:
                trail.pop(0)

            draw_glowing_nose_point(frame, nose_point)

            if (center_x - 50 < nose_point[0] < center_x + 50 and
                center_y - 50 < nose_point[1] < center_y + 50):
                if center_hold_start is None:
                    center_hold_start = time.time()
                elif time.time() - center_hold_start >= BACK_HOLD_SECONDS:
                    draw_centered_text(frame, "Returning to Main UI...", h // 2, scale=1.2, color=(0, 0, 255), thickness=3)
                    cv2.imshow("Face Pattern Lock", frame)
                    cv2.waitKey(1000)
                    cap.release()
                    cv2.destroyAllWindows()
                    try:
                        import mainUI
                    except ImportError:
                        subprocess.run(['python', 'mainUI.py'])
                    exit()
            else:
                center_hold_start = None

            if time.time() - last_gesture_time > PAUSE_SECONDS and len(trail) >= 2:
                d = get_direction(trail[-2], trail[-1])
                if d in ['left', 'right']:
                    direction_sequence.append(d)
                    last_gesture_time = time.time()
                    print(f"[Gesture] Detected: {d}")
                    if len(direction_sequence) > PATTERN_LENGTH:
                        direction_sequence.pop(0)

                    if len(direction_sequence) == PATTERN_LENGTH:
                        if direction_sequence == EASY_PATTERN:
                            unlocked = True
                            show_message = True
                            message_time = time.time()
                            print("[SUCCESS] Pattern matched. Locking system...")
                        else:
                            incorrect_attempt = True
                            message_time = time.time()
                            direction_sequence.clear()
                            print("[ERROR] Incorrect pattern.")

        draw_pulsating_circle(frame, (center_x, center_y), elapsed, base_radius=50, color=(255, 0, 255))

        draw_centered_text(frame, f"Current Path: {direction_sequence}", 40, scale=0.8, color=(255, 255, 0))

        if show_message and unlocked:
            draw_centered_text(frame, "Pattern Matched. Locking System...", h // 2, scale=1.1, color=(0, 255, 0), thickness=3)
            if time.time() - message_time >= 2:
                lock_system()
                break
        elif incorrect_attempt:
            draw_centered_text(frame, "Incorrect Attempt! Try Again", h // 2, scale=1.2, color=(0, 0, 255), thickness=3)
            if time.time() - message_time >= 2:
                incorrect_attempt = False
        else:
            draw_centered_text(frame, "Turn Head right left right to Lock the System", h - 60, scale=0.8, color=(0, 255, 200), thickness=2)
            draw_centered_text(frame, "Hold Nose at Center to Exit", h - 30, scale=0.8, color=(255, 150, 255), thickness=2)

        cv2.imshow("Neuro-Face Lock System (Hold Nose at Centre to Exit)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[EXIT] User exited.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_face_pattern_lock()
