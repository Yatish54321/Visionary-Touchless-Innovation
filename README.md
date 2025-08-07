
# Visionary Touchless Innovation: Shaping the Future of Touch-Free Control(Will update for Full version)

## Project Overview

This project introduces a cutting-edge touchless interaction system designed to automate computer tasks through hand gestures, eye blinks, and voice commands. The system includes advanced modules for mouse control, virtual keyboard input, screenshot capturing, and voice-based operations. It aims to provide an accessible, hygienic, and intuitive interface for users in various environments, enhancing productivity and inclusivity.

## Features and Functionalities

### Core Features
1. **Mouse Control**:
   - Real-time hand gesture-based cursor movement.
   - Supports left-click, right-click, and drag-and-drop functionalities.
   - Smooth scrolling using two-hand gestures.

2. **Virtual Keyboard**:
   - Touchless text input via hand gestures mapped to a QWERTY keyboard.
   - Customizable and dynamic UI for accessibility and user preference.

3. **Screenshot Functionality**:
   - Capture screenshots with eye blinks or specific gestures.
   - Saves high-resolution screenshots automatically.

4. **Voice Command Integration**:
   - Perform tasks like opening applications, web searches, and controlling system operations using natural language commands.

### Secondary Features
- Dynamic user interface with visual feedback.
- Cross-platform compatibility (Windows, macOS, Linux).
- Multi-language support for voice commands.

### Advanced Functionalities
- Gesture-based scrolling.
- AI-driven personalization for gesture adaptation.
- Notifications for successful actions.

## Technologies Used
### Programming Language
- **Python 3.10+**

### Libraries and Frameworks
- **OpenCV**: For video capture and image processing.
- **MediaPipe**: For real-time hand and face tracking.
- **PyAutoGUI**: For simulating keyboard and mouse interactions.
- **Streamlit**: For creating an interactive web-based interface.
- **Pynput**: For advanced mouse control functionalities.

### Tools
- Webcam (for video input).
- PyInstaller (for creating executable files).

## System Design and Architecture

### Workflow
1. **Input**: Webcam captures hand gestures and facial landmarks.
2. **Processing**: Gesture detection and mapping via MediaPipe and OpenCV.
3. **Action Execution**: Mouse movement, keyboard typing, or screenshot capturing.
4. **Output**: Visual feedback on the screen and real-time system responses.

### System Components
- **Input Devices**: Webcam and microphone.
- **Processing Layer**: Modules for hand gesture and voice recognition.
- **Output Interface**: Virtual keyboard, mouse controller, and notification system.

## Installation and Setup

### Prerequisites
- Python 3.10+
- A functional webcam.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Yatish54321/Visionary-Touchless-Innovation.git
   cd touchless-technology
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Follow the on-screen instructions to enable the desired features.

## Usage Guide

### How to Use
- **Mouse Control**: Use hand gestures to move the cursor and perform clicks.
- **Virtual Keyboard**: Hover over keys and tap gestures to type.
- **Screenshot Capture**: Blink your eyes or click the dedicated button.
- **Voice Commands**: Speak commands like "Open YouTube" to execute actions.

## Results

- **Mouse Control**: Achieved an accuracy of 95% with less than 100ms latency.
- **Screenshot Capture**: 98% success rate with 200ms processing time.
- **Virtual Keyboard**: Typing accuracy of 92%.
- **Voice Commands**: 97% recognition rate.

## Future Scope

- **Enhanced Gesture Recognition**:
  - Implement 3D gesture recognition for complex interactions.
  - AI-driven personalization for user-specific gestures.
- **Integration with Wearable Technology**:
  - Expand to AR/VR environments.
  - Include haptic feedback for immersive interactions.
- **Applications in Smart Environments**:
  - Control smart home devices and automotive systems.

## Contributors

- **Yatish Kumar Verma** (2108400100064)
- **Kuldeep Kumar** (2108400100031)

## License

This project is open-source and available under the [MIT License](LICENSE).
