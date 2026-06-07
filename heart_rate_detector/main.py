import cv2
import numpy as np

from eye_tracker import EyeTracker
from pulse_detector import PulseDetector

tracker = EyeTracker()
pulse = PulseDetector()

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


def draw_signal(canvas, signal):

    if len(signal) < 10:
        return

    signal = np.array(signal)

    signal = signal - np.mean(signal)

    max_val = np.max(np.abs(signal))

    if max_val == 0:
        return

    signal = signal / max_val

    # Grid
    for x in range(20, 500, 50):
        cv2.line(canvas, (x, 140), (x, 300), (40, 40, 40), 1)

    for y in range(140, 300, 30):
        cv2.line(canvas, (20, y), (500, y), (40, 40, 40), 1)

    for i in range(len(signal) - 1):

        x1 = 20 + i * 4
        y1 = 220 - int(signal[i] * 70)

        x2 = 20 + (i + 1) * 4
        y2 = 220 - int(signal[i + 1] * 70)

        cv2.line(
            canvas,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )


def draw_fft(canvas, fft_data):

    if len(fft_data) < 5:
        return

    fft_data = np.array(fft_data)

    max_fft = np.max(fft_data)

    if max_fft == 0:
        return

    fft_data = fft_data / max_fft

    # Grid
    for x in range(20, 500, 50):
        cv2.line(canvas, (x, 330), (x, 470), (40, 40, 40), 1)

    for y in range(330, 470, 30):
        cv2.line(canvas, (20, y), (500, y), (40, 40, 40), 1)

    for i in range(min(len(fft_data) - 1, 100)):

        x1 = 20 + i * 4
        y1 = 470 - int(fft_data[i] * 120)

        x2 = 20 + (i + 1) * 4
        y2 = 470 - int(fft_data[i + 1] * 120)

        cv2.line(
            canvas,
            (x1, y1),
            (x2, y2),
            (0, 200, 255),
            2
        )


while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Mirror webcam
    frame = cv2.flip(frame, 1)

    frame = cv2.resize(
        frame,
        (640, 480)
    )

    frame, roi = tracker.detect_eye_region(frame)

    bpm = 0
    freq = 0.0

    if roi is not None and roi.size > 0:

        metrics = pulse.update(roi)

        bpm = metrics["bpm"]
        freq = metrics["frequency"]

    # Dashboard
    dashboard = np.full(
        (480, 500, 3),
        (15, 15, 15),
        dtype=np.uint8
    )

    cv2.putText(
        dashboard,
        "HEART RATE MONITOR",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    cv2.putText(
        dashboard,
        f"{bpm}",
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 0),
        3
    )

    cv2.putText(
        dashboard,
        "BPM",
        (180, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        dashboard,
        f"Frequency: {freq:.2f} Hz",
        (20, 130),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.line(
        dashboard,
        (10, 145),
        (490, 145),
        (70, 70, 70),
        1
    )

    cv2.putText(
        dashboard,
        "PULSE SIGNAL",
        (20, 170),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    cv2.putText(
        dashboard,
        "FFT SPECTRUM",
        (20, 320),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    draw_signal(
        dashboard,
        pulse.get_signal()
    )

    draw_fft(
        dashboard,
        pulse.get_fft()
    )

    combined = np.hstack(
        (frame, dashboard)
    )

    cv2.namedWindow(
        "Heart Rate & Pulse Monitor",
        cv2.WINDOW_NORMAL
    )

    cv2.imshow(
        "Heart Rate & Pulse Monitor",
        combined
    )

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()