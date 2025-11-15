# drawer.py – 绘制关键点、骨架、角度和手势（表格显示角度）
import cv2
import math

# 手骨架连接
HAND_CONNECTIONS = [
    (1, 2), (2, 3), (3, 4),      # 拇指
    (5, 6), (6, 7), (7, 8),      # 食指
    (9, 10), (10, 11), (11, 12), # 中指
    (13, 14), (14, 15), (15, 16),# 无名指
    (17, 18), (18, 19), (19, 20),# 小指
    (0, 5), (0, 9), (0, 13), (0, 17)
]

class Drawer:
    def __init__(self):
        pass

    def draw_landmarks(self, frame, hand):
        for lm in hand.landmark:
            x = int(lm.x * frame.shape[1])
            y = int(lm.y * frame.shape[0])
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    def draw_connections(self, frame, hand):
        for start, end in HAND_CONNECTIONS:
            x1 = int(hand.landmark[start].x * frame.shape[1])
            y1 = int(hand.landmark[start].y * frame.shape[0])
            x2 = int(hand.landmark[end].x * frame.shape[1])
            y2 = int(hand.landmark[end].y * frame.shape[0])
            cv2.line(frame, (x1, y1), (x2, y2), (0, 200, 255), 2)

    # ----------------------
    # 计算三点夹角
    # ----------------------
    def calculate_angle(self, a, b, c):
        """
        a,b,c: mediapipe landmark
        夹角在b点
        """
        ba = [a.x - b.x, a.y - b.y]
        bc = [c.x - b.x, c.y - b.y]
        dot = ba[0]*bc[0] + ba[1]*bc[1]
        norm_ba = math.sqrt(ba[0]**2 + ba[1]**2)
        norm_bc = math.sqrt(bc[0]**2 + bc[1]**2)
        if norm_ba * norm_bc == 0:
            return 0
        angle = math.acos(dot / (norm_ba * norm_bc))
        return math.degrees(angle)

    # ----------------------
    # 生成手指角度字典
    # ----------------------
    def get_finger_angles(self, hand):
        finger_joints = {
            "Thumb": [1, 2, 3, 4],
            "Index": [5, 6, 7, 8],
            "Middle": [9, 10, 11, 12],
            "Ring": [13, 14, 15, 16],
            "Pinky": [17, 18, 19, 20]
        }
        angles_dict = {}
        for finger, joints in finger_joints.items():
            a = hand.landmark[joints[0]]
            b = hand.landmark[joints[1]]
            c = hand.landmark[joints[2]]
            angle1 = self.calculate_angle(a, b, c)

            a = hand.landmark[joints[1]]
            b = hand.landmark[joints[2]]
            c = hand.landmark[joints[3]]
            angle2 = self.calculate_angle(a, b, c)

            # 保存到字典
            angles_dict[finger] = (int(angle1), int(angle2))
        return angles_dict

    # ----------------------
    # 在左下角绘制角度表格
    # ----------------------
    def draw_angle_table(self, frame, angles_dict):
        """
        angles_dict: {finger_name: (angle1, angle2)}
        可自定义表格位置和字体大小
        """
        # ----------------------
        # 可自定义：表格位置、字体、颜色
        start_x = 10                 # 左下角 x 坐标
        start_y = frame.shape[0] - 150 # 左下角 y 坐标
        line_height = 25
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        color = (255, 255, 255)  # 自定义颜色
        thickness = 1
        # ----------------------

        y = start_y
        cv2.putText(frame, "Finger Angles:", (start_x, y), font, font_scale+0.1, color, 2)
        y += line_height

        for finger, (angle1, angle2) in angles_dict.items():
            text = f"{finger}: {angle1}, {angle2}"
            cv2.putText(frame, text, (start_x, y), font, font_scale, color, thickness)
            y += line_height

