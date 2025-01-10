import cv2
import mediapipe as mp
import pyautogui  # For simulating keyboard inputs

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# Define QWERTY keyboard layout
keyboard_layout = [
    ["Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "Del"],
    ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace"],
    ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
    ["CapsLock", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter"],
    ["Shift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "Shift"],
    ["Ctrl", "Alt", "Space", "Alt", "Ctrl"]
]

# Small key dimensions and spacing
key_width = 35
key_height = 35
key_margin = 5
functional_key_width = 70  # Larger functional keys
space_key_width = 150  # Width of the Space bar

# Function to draw a transparent, small keyboard
def draw_keyboard(frame, layout, start_x, start_y):
    for row_index, row in enumerate(layout):
        for col_index, key in enumerate(row):
            # Calculate key width for functional keys
            if key in ["Space", "Enter", "Shift"]:
                width = space_key_width if key == "Space" else functional_key_width
            else:
                width = key_width

            # Calculate key position
            x = start_x + col_index * (key_width + key_margin)
            y = start_y + row_index * (key_height + key_margin)

            # Adjust position for Space bar
            if key == "Space":
                x += key_margin * 2

            # Create a transparent key
            overlay = frame.copy()
            color = (50, 50, 50) if key not in ["Space", "Enter", "Shift", "Backspace"] else (255, 100, 100)
            cv2.rectangle(overlay, (x, y), (x + width, y + key_height), color, -1, cv2.LINE_AA)
            alpha = 0.4  # Lower alpha value for transparency
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

            # Highlight hovered key with higher alpha
            if hovered_key == key:
                cv2.rectangle(frame, (x, y), (x + width, y + key_height), (0, 255, 255), -1, cv2.LINE_AA)

            # Draw key label
            font_scale = 0.4 if len(key) <= 1 else 0.3
            text_x = x + (width // 2) - (len(key) * int(font_scale * 7))  # Center text horizontally
            text_y = y + key_height // 2 + 8  # Center text vertically
            cv2.putText(frame, key, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 1)

# Detect hovered key
def detect_hover_key(hand_landmarks, frame_width, frame_height, layout, start_x, start_y):
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_x, index_y = int(index_tip.x * frame_width), int(index_tip.y * frame_height)

    # Draw a dynamic cursor at the index finger position
    cv2.circle(frame, (index_x, index_y), 10, (0, 255, 255), -1)

    for row_index, row in enumerate(layout):
        for col_index, key in enumerate(row):
            if key in ["Space", "Enter", "Shift"]:
                width = space_key_width if key == "Space" else functional_key_width
            else:
                width = key_width

            # Calculate key position
            x = start_x + col_index * (key_width + key_margin)
            y = start_y + row_index * (key_height + key_margin)

            if x < index_x < x + width and y < index_y < y + key_height:
                return key
    return None

# Detect tap gesture
def detect_tap(hand_landmarks, frame_width, frame_height):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    thumb_x, thumb_y = int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height)
    index_x, index_y = int(index_tip.x * frame_width), int(index_tip.y * frame_height)

    tolerance = max(key_width, key_height) // 2  # Adjust sensitivity
    return abs(thumb_x - index_x) < tolerance and abs(thumb_y - index_y) < tolerance

# Start video capture
cap = cv2.VideoCapture(0)
typed_text = ""  # Store the typed text
hovered_key = None

cv2.namedWindow('Compact Keyboard', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Compact Keyboard', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip and process the frame
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame_height, frame_width, _ = frame.shape
    keyboard_width = len(keyboard_layout[0]) * (key_width + key_margin) - key_margin
    keyboard_height = len(keyboard_layout) * (key_height + key_margin) - key_margin
    start_x = (frame_width - keyboard_width) // 2
    start_y = (frame_height - keyboard_height - 100)  # Adjust space for text

    # Process hand landmarks
    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            hovered_key = detect_hover_key(hand_landmarks, frame_width, frame_height, keyboard_layout, start_x, start_y)
            if hovered_key and detect_tap(hand_landmarks, frame_width, frame_height):
                if hovered_key == "Backspace":
                    typed_text = typed_text[:-1]
                elif hovered_key == "Space":
                    typed_text += " "
                elif hovered_key == "Enter":
                    typed_text += "\n"
                elif hovered_key == "Del":
                    typed_text = ""
                else:
                    typed_text += hovered_key

    # Draw keyboard
    draw_keyboard(frame, keyboard_layout, start_x, start_y)

    # Display typed text
    cv2.putText(frame, f"Typed Text: {typed_text}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow('Compact Keyboard', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
