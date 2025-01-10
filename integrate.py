import streamlit as st
import threading
import cv2
import mediapipe as mp
import pyautogui  # For controlling the mouse
from pynput.mouse import Controller, Button
from multiprocessing import Process
import time

# Importing the separate modules for keyboard, mic, screenshot
from code1 import run as keyboard_control
from voice_control import run as mic_control
from screenshot import run as screenshot_control

# Initialize Mediapipe Hands and mouse controller
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mouse = Controller()


# Main Mouse Control Model
class MouseControl:
    def __init__(self):
        self.hand_gesture_recognition = HandGestureRecognition()

    def start_mouse_control(self):
        # Start the webcam feed
        video_feed = cv2.VideoCapture(0)

        # Start hand gesture recognition in a separate thread
        gesture_thread = threading.Thread(target=self.hand_gesture_recognition.recognize_gesture, args=(video_feed,))
        gesture_thread.start()

        # Main loop for controlling the mouse
        while True:
            # Logic to handle the hand gestures and perform the mouse control
            pass

    def run(self):
        self.start_mouse_control()


# Separate module for hand gesture recognition
class HandGestureRecognition:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils

    def recognize_gesture(self, video_feed):
        prev_distance = 0  # To track the previous distance for scrolling
        while True:
            ret, frame = video_feed.read()
            if not ret:
                continue

            # Flip and process the frame
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            # Extract hand landmarks
            hand_positions = []
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                    # Get index finger, middle finger, and thumb tip landmarks
                    index_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                    middle_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

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
        video_feed.release()
        cv2.destroyAllWindows()


# Streamlit UI Setup
def display_icons():
    st.set_page_config(page_title="Mouse Control System", page_icon="🖱️")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Virtual Keyboard"):
            st.session_state.page = "keyboard"  # Navigate to keyboard control
    with col2:
        if st.button("Microphone"):
            st.session_state.page = "mic"  # Navigate to microphone control
    with col3:
        if st.button("Screenshot"):
            st.session_state.page = "screenshot"  # Navigate to screenshot control


def back_button():
    if st.button("Back"):
        st.session_state.page = "mouse_control"  # Go back to the main mouse control page


def mouse_control_page():
    # Initialize the Mouse Control System
    mouse_control = MouseControl()

    # Start mouse control
    mouse_control.run()


def main():
    if "page" not in st.session_state:
        st.session_state.page = "mouse_control"  # Default page

    if st.session_state.page == "mouse_control":
        # Display the main mouse control system with buttons
        display_icons()
        mouse_control_page()

    elif st.session_state.page == "keyboard":
        back_button()
        # Running the keyboard control in a separate process for better performance
        keyboard_process = Process(target=keyboard_control)
        keyboard_process.start()
        keyboard_process.join()

    elif st.session_state.page == "mic":
        back_button()
        # Running the mic control in a separate process for better performance
        mic_process = Process(target=mic_control)
        mic_process.start()
        mic_process.join()

    elif st.session_state.page == "screenshot":
        back_button()
        # Running the screenshot control in a separate process for better performance
        screenshot_process = Process(target=screenshot_control)
        screenshot_process.start()
        screenshot_process.join()


if __name__ == "__main__":
    main()
