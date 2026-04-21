import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False)

def get_hand_landmarks(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:

            x_list = []
            y_list = []

            for lm in handLms.landmark:
                x_list.append(lm.x)
                y_list.append(lm.y)

            # SAME NORMALIZATION AS TRAINING
            min_x = min(x_list)
            min_y = min(y_list)

            landmarks = []
            for x, y in zip(x_list, y_list):
                landmarks.append(x - min_x)
                landmarks.append(y - min_y)

            return landmarks

    return None