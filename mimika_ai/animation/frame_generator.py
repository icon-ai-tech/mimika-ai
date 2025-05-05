import numpy as np
import cv2
from typing import List

class FrameGenerator:
    def __init__(self, base_image_path: str, frame_size: tuple = (512, 512)):
        self.base_image = cv2.imread(base_image_path)
        if self.base_image is None:
            raise FileNotFoundError(f"Base image not found at {base_image_path}")
        self.frame_size = frame_size
        self.base_image = cv2.resize(self.base_image, frame_size)

    def apply_landmarks(self, landmarks: List[np.ndarray]) -> List[np.ndarray]:
        frames = []
        for lm in landmarks:
            frame = self.base_image.copy()
            for (x, y) in lm:
                cv2.circle(frame, (int(x), int(y)), 2, (0, 255, 0), -1)
            frames.append(frame)
        return frames
