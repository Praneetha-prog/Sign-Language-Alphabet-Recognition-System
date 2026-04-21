import cv2
import csv
from detector import get_hand_landmarks

cap = cv2.VideoCapture(0)

label = input("Enter label (A-Z): ")

with open("dataset.csv", "a", newline="") as f:
    writer = csv.writer(f)

    while True:
        ret, frame = cap.read()
        landmarks, frame = get_hand_landmarks(frame)

        if len(landmarks) == 42:
            writer.writerow(landmarks + [label])
            print("Saved")

        cv2.imshow("Collecting Data", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()