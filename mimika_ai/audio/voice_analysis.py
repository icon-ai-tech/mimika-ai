import numpy as np
import librosa

class VoiceAnalyzer:
    def __init__(self, sr: int = 16000):
        self.sr = sr

    def extract_pitch(self, audio: np.ndarray) -> np.ndarray:
        pitches, magnitudes = librosa.piptrack(y=audio, sr=self.sr)
        pitch_track = []
        for i in range(pitches.shape[1]):
            index = magnitudes[:, i].argmax()
            pitch = pitches[index, i]
            pitch_track.append(pitch)
        return np.array(pitch_track)

    def get_energy(self, audio: np.ndarray) -> float:
        return float(np.mean(audio ** 2))
