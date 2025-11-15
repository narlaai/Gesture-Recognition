# utils/camera.py – 摄像头工具类（按比例缩放填充窗口）
import cv2

class Camera:
    def __init__(self, index=0, window_name="Camera"):
        self.cap = cv2.VideoCapture(index)
        self.window_name = window_name
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)  # 可手动调整窗口

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def show(self, frame):
        """
        显示视频帧，并按窗口大小自动缩放，保持宽高比
        """
        # 获取窗口当前大小
        try:
            _, _, win_width, win_height = cv2.getWindowImageRect(self.window_name)
        except AttributeError:
            # 如果 OpenCV 版本过低，不支持 getWindowImageRect，使用默认大小
            win_width, win_height = frame.shape[1], frame.shape[0]

        # 获取帧原始宽高
        frame_height, frame_width = frame.shape[:2]

        # 计算缩放比例（保持宽高比）
        scale_w = win_width / frame_width
        scale_h = win_height / frame_height
        scale = min(scale_w, scale_h)

        # 计算缩放后的尺寸
        new_width = int(frame_width * scale)
        new_height = int(frame_height * scale)

        # 缩放帧
        frame_resized = cv2.resize(frame, (new_width, new_height))

        # 创建黑色背景填充窗口
        canvas = cv2.resize(frame, (win_width, win_height)) * 0  # 全黑
        # 或使用 np.zeros((win_height, win_width, 3), dtype=np.uint8)
        import numpy as np
        canvas = np.zeros((win_height, win_width, 3), dtype=np.uint8)

        # 计算居中位置
        x_offset = (win_width - new_width) // 2
        y_offset = (win_height - new_height) // 2

        # 把缩放帧贴到黑色背景中心
        canvas[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = frame_resized

        cv2.imshow(self.window_name, canvas)

    def should_quit(self):
        key = cv2.waitKey(1) & 0xFF
        return key == ord('q')  # 按 q 键退出

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
