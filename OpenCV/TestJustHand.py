import cv2
from cvzone.HandTrackingModule import HandDetector
import time

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)

# stores the finger
hand_states = [["Wrist", False],
               ["Index", False],
               ["Middle", False],
               ["Ring", False],
               ["Thumb", False],
               ["Pinky", False]]

prev_time = 0

while True:
    success, frame = cap.read()
    if not success:
        break

    # finds hands
    hands, frame = detector.findHands(frame, draw=True)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        # list of 21 landmark positions
        if len(lmList) >= 21:
            j = 1
            change = False

            # loop through all fingers with 1 being the thumb
            for i in range(1, 6):
                if i == 1:
                    if lmList[4][0] < lmList[3][0] and not hand_states[4][1]:
                        hand_states[4][1] = True
                        change = True
                        print(hand_states[4][0], hand_states[4][1])
                    elif lmList[4][0] > lmList[3][0] and hand_states[4][1]:
                        hand_states[4][1] = False
                        change = True
                        print(hand_states[4][0], hand_states[4][1])
                else:
                    # other fingers (not thumn)
                    tip_id = i * 4
                    lower_joint_id = tip_id - 2
                    if lmList[tip_id][1] > lmList[lower_joint_id][1] and not hand_states[j][1]:
                        hand_states[j][1] = True
                        change = True
                        print(hand_states[j][0], hand_states[j][1])
                    elif lmList[tip_id][1] < lmList[lower_joint_id][1] and hand_states[j][1]:
                        hand_states[j][1] = False
                        change = True
                        print(hand_states[j][0], hand_states[j][1])

                    if j == 3:
                        j += 2
                    else:
                        j += 1

            # if theres a change detected, send new data to Arduino
            if change:
                msg = ""
                for i in range(6):
                    msg += "1" if hand_states[i][1] else "0"
                msg += "\n"
                print("Sending:", msg.strip())

    # calculate FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time else 0
    prev_time = curr_time

    cv2.putText(frame, f"FPS: {int(fps)}", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 3)

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

