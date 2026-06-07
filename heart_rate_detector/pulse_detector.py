import numpy as np
from scipy.signal import butter, filtfilt

class PulseDetector:

    def __init__(self):

        self.signal = []
        self.filtered_signal = []
        self.fft_data = []

    def update(self, roi):

        green = np.mean(roi[:, :, 1])

        self.signal.append(green)

        if len(self.signal) > 450:
            self.signal.pop(0)

        return self.calculate()

    def calculate(self):

        if len(self.signal) < 150:

            return {
                "bpm": 0,
                "frequency": 0
            }

        signal = np.array(self.signal)

        signal = signal - np.mean(signal)

        fs = 30

        low = 0.8 / (fs / 2)
        high = 3.0 / (fs / 2)

        b, a = butter(
            3,
            [low, high],
            btype='band'
        )

        filtered = filtfilt(
            b,
            a,
            signal
        )

        self.filtered_signal = filtered.tolist()

        fft = np.abs(np.fft.rfft(filtered))

        freqs = np.fft.rfftfreq(
            len(filtered),
            d=1/fs
        )

        self.fft_data = fft.tolist()

        idx = np.argmax(fft)

        frequency = freqs[idx]

        bpm = frequency * 60

        return {
            "bpm": round(bpm, 1),
            "frequency": round(frequency, 2)
        }

    def get_signal(self):

        return self.filtered_signal[-120:]

    def get_fft(self):

        return self.fft_data[:120]