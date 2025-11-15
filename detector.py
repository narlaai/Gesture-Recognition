# detector.py – 使用经典 MediaPipe Hands API
import cv2
import mediapipe as mp
import config

class HandDetector:
    def __init__(self, max_hands=None):
        if max_hands is None:
            max_hands = config.MAX_HANDS

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def detect(self, frame):
        """
        输入 BGR 图像，输出关键点列表
        返回 results.multi_hand_landmarks 或 None
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        return results.multi_hand_landmarks
