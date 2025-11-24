This is the code for the robotic hand.

You must download the libraries from requirements. Write this in the terminal:

- py -m venv .venv
- .\.venv\Scripts\activate
- pip install -r requirements.txt


There are three main folders to look at:
- BasicMotorControl (C++)
    - Write commands to the serial monitor to control the angle of the servo.
    - How to run?
        - Run Hand.ino via Arduino IDE and write commands in that IDE serial monitor

- OpenCV (C++ and Python)
    - Detects hand through the computer's web cam and ouputs binary to Arduino via serial
    - How to run?
        - Upload HandReceiveCV.ino to Arduino via Arduino IDE
        - Close Arduino IDE (important to close that serial connection for next step)
        - Run HandDetector.py to run the CV side

- Robot (Python application)
    - A GUI app to control the hand
    - How to run?
        - Upload HandReceiveCV.ino to Arduino via Arduino IDE
        - Run app.py and control via the buttons/labels

