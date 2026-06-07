import cv2
import numpy as np

class EyeTracker:

    def __init__(self):

        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_eye.xml"
        )

    def detect_eye_region(self, frame):

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        eyes = self.eye_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        rois = []

        # Sort eyes from left to right
        eyes = sorted(eyes, key=lambda e: e[0])

        # Take first two eyes
        for (x, y, w, h) in eyes[:2]:

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "Eye",
                (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1
            )

            eye_roi = frame[
                y:y+h,
                x:x+w
            ]

            if eye_roi.size > 0:
                rois.append(eye_roi)

        roi = None

        # Both eyes detected
        if len(rois) == 2:

            h = min(
                rois[0].shape[0],
                rois[1].shape[0]
            )

            roi1 = cv2.resize(
                rois[0],
                (rois[0].shape[1], h)
            )

            roi2 = cv2.resize(
                rois[1],
                (rois[1].shape[1], h)
            )

            roi = np.hstack(
                (roi1, roi2)
            )

        # One eye detected
        elif len(rois) == 1:

            roi = rois[0]

        return frame, roi