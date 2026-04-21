import cv2
import mediapipe as mp
import os
import csv

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True)

DATASET_PATH = "asl_images"

with open("dataset.csv", "w", newline="") as f:
    writer = csv.writer(f)

    for label in os.listdir(DATASET_PATH):
        folder = os.path.join(DATASET_PATH, label)

        # limit images for speed
        for img_name in os.listdir(folder)[:100]:
            img_path = os.path.join(folder, img_name)

            img = cv2.imread(img_path)
            if img is None:
                continue

            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            if result.multi_hand_landmarks:
                for handLms in result.multi_hand_landmarks:

                    x_list = []
                    y_list = []

                    # collect all points
                    for lm in handLms.landmark:
                        x_list.append(lm.x)
                        y_list.append(lm.y)

                    # normalize
                    min_x = min(x_list)
                    min_y = min(y_list)

                    landmarks = []
                    for x, y in zip(x_list, y_list):
                        landmarks.append(x - min_x)
                        landmarks.append(y - min_y)

                    if len(landmarks) == 42:
                        writer.writerow(landmarks + [label])

print("Dataset created!")