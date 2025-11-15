import cv2
from detector import HandDetector
from drawer import Drawer
from utils.camera import Camera
import config

def main():
    cam = Camera(config.CAMERA_INDEX, config.WINDOW_NAME)
    detector = HandDetector(config.MAX_HANDS)
    drawer = Drawer()

    while True:
        frame = cam.read()
        if frame is None:
            break

        results = detector.detect(frame)

        if results:
            for hand in results:
                drawer.draw_landmarks(frame, hand)
                drawer.draw_connections(frame, hand)

                # 获取角度字典
                angles_dict = drawer.get_finger_angles(hand)

                # 在左下角绘制表格
                drawer.draw_angle_table(frame, angles_dict)

        cam.show(frame)

        if cam.should_quit():
            break

    cam.release()

if __name__ == "__main__":
    main()
