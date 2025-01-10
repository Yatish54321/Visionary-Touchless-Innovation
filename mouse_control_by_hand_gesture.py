import cv2
import mediapipe as mp
from pynput.mouse import Controller, Button

# Initialize Mediapipe Hands and mouse controller
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mouse = Controller()

# OpenCV video capture
cap = cv2.VideoCapture(0)

# Mediapipe Hands configuration
with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    prev_distance = 0  # To track the previous distance for scrolling

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to access camera.")
            break

        # Flip and process the frame
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # Extract hand landmarks
        if results.multi_hand_landmarks:
            hand_positions = []
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get index finger, middle finger, and thumb tip landmarks
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

                # Convert normalized coordinates to pixel values
                h, w, _ = frame.shape
                index_x, index_y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
                thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
                middle_x, middle_y = int(middle_finger_tip.x * w), int(middle_finger_tip.y * h)

                hand_positions.append((index_x, index_y, thumb_x, thumb_y, middle_x, middle_y))

            if len(hand_positions) >= 1:
                # Handle single hand mouse control
                hand = hand_positions[0]
                index_x, index_y, thumb_x, thumb_y, middle_x, middle_y = hand

                # Move mouse pointer to index finger position
                screen_w, screen_h = 1920, 1080  # Adjust screen resolution
                mouse.position = (index_x * screen_w // w, index_y * screen_h // h)

                # Detect left click gesture (index and thumb close together)
                distance_thumb_index = ((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2) ** 0.5
                if distance_thumb_index < 30:  # Threshold distance for left-click
                    mouse.click(Button.left, 1)

                # Detect right click gesture (index and middle finger close together)
                distance_index_middle = ((index_x - middle_x) ** 2 + (index_y - middle_y) ** 2) ** 0.5
                if distance_index_middle < 30:  # Threshold distance for right-click
                    mouse.click(Button.right, 1)

            if len(hand_positions) == 2:
                # Extract positions for two hands
                hand1 = hand_positions[0]
                hand2 = hand_positions[1]
                index_x1, index_y1, thumb_x1, thumb_y1, middle_x1, middle_y1 = hand1
                index_x2, index_y2, thumb_x2, thumb_y2, middle_x2, middle_y2 = hand2

                # Calculate the vertical distance between the two index fingers
                vertical_distance = abs(index_y1 - index_y2)

                # Set scrolling sensitivity and speed
                scroll_sensitivity = 15  # The sensitivity for scrolling speed

                # Check for scroll direction based on hand position
                if index_y1 > index_y2:  # Hand 1 is below Hand 2, scrolling down
                    scroll_amount = vertical_distance // scroll_sensitivity
                    mouse.scroll(0, -scroll_amount)  # Scroll down
                elif index_y1 < index_y2:  # Hand 1 is above Hand 2, scrolling up
                    scroll_amount = vertical_distance // scroll_sensitivity
                    mouse.scroll(0, scroll_amount)  # Scroll up

        # Display the webcam feed
        cv2.imshow("Hand Gesture Mouse Control", frame)

        # Exit loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
