import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Blink Detection Thresholds
BLINK_THRESHOLD = 0.2
CONSECUTIVE_FRAMES = 3

# Function to calculate the eye aspect ratio (EAR)
def calculate_eye_aspect_ratio(landmarks, eye_indices):
    vertical_1 = np.linalg.norm(np.array(landmarks[eye_indices[1]]) - np.array(landmarks[eye_indices[5]]))
    vertical_2 = np.linalg.norm(np.array(landmarks[eye_indices[2]]) - np.array(landmarks[eye_indices[4]]))
    horizontal = np.linalg.norm(np.array(landmarks[eye_indices[0]]) - np.array(landmarks[eye_indices[3]]))
    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
    return ear

# Function to capture a screenshot
def capture_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save(f"screenshot_{int(time.time())}.png")
    print("Screenshot saved!")

# Function to apply the dotted mask
def apply_uniform_dotted_mask(frame, landmarks):
    dot_color = (255, 0, 0)  # Blue color (BGR)
    dot_radius = 2  # Small dots for a clean mask
    for x, y in landmarks:
        cv2.circle(frame, (x, y), dot_radius, dot_color, -1)

# Main function
def main():
    cap = cv2.VideoCapture(0)
    blink_counter = 0
    screenshot_taken = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame for a mirrored effect
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # Convert the frame to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Extract landmarks
                landmarks = [(int(lm.x * w), int(lm.y * h)) for lm in face_landmarks.landmark]

                # Eye indices for blink detection
                left_eye_indices = [33, 160, 158, 133, 153, 144]
                right_eye_indices = [362, 385, 387, 263, 373, 380]

                # Calculate EAR for both eyes
                left_ear = calculate_eye_aspect_ratio(landmarks, left_eye_indices)
                right_ear = calculate_eye_aspect_ratio(landmarks, right_eye_indices)

                # Average EAR for both eyes
                avg_ear = (left_ear + right_ear) / 2.0

                # Blink detection logic
                if avg_ear < BLINK_THRESHOLD:
                    blink_counter += 1
                else:
                    if blink_counter >= CONSECUTIVE_FRAMES:
                        if not screenshot_taken:
                            print("Blink detected! Taking screenshot...")
                            capture_screenshot()
                            screenshot_taken = True
                    blink_counter = 0
                    screenshot_taken = False

                # Apply uniform dotted mask
                apply_uniform_dotted_mask(frame, landmarks)

        # Display the frame with the dotted mask
        cv2.imshow("Dotted Face Mask with Blink Detection", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
