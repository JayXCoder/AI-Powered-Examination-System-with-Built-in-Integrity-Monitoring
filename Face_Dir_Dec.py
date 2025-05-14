import cv2
import mediapipe as mp
import numpy as np
import os
from datetime import datetime

class GazeMonitor:
    def __init__(self, warning_threshold=1.5):
        print("[DEBUG] Initializing GazeMonitor class...")
        self.warning_threshold = warning_threshold
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False,
                                                         max_num_faces=1,
                                                         refine_landmarks=True,
                                                         min_detection_confidence=0.5,
                                                         min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_face_mesh = mp.solutions.face_mesh
        self.logs_path = "gaze_logs"
        os.makedirs(self.logs_path, exist_ok=True)

    def get_head_pose(self, image_points, w, h):
        model_points = np.array([
            (0.0, 0.0, 0.0),             # Nose tip
            (0.0, -330.0, -65.0),        # Chin
            (-225.0, 170.0, -135.0),     # Left eye left corner
            (225.0, 170.0, -135.0),      # Right eye right corner
            (-150.0, -150.0, -125.0),    # Left mouth corner
            (150.0, -150.0, -125.0)      # Right mouth corner
        ], dtype="double")

        focal_length = w
        center = (w / 2, h / 2)
        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype="double")

        dist_coeffs = np.zeros((4, 1))
        success, rotation_vector, _ = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs)
        rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
        sy = np.sqrt(rotation_matrix[0, 0] ** 2 + rotation_matrix[1, 0] ** 2)
        singular = sy < 1e-6

        if not singular:
            x = np.arctan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
            y = np.arctan2(-rotation_matrix[2, 0], sy)
            z = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
        else:
            x = np.arctan2(-rotation_matrix[1, 2], rotation_matrix[1, 1])
            y = np.arctan2(-rotation_matrix[2, 0], sy)
            z = 0

        return np.degrees(x), np.degrees(y), np.degrees(z)

    def log_violation(self, frame, status):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.logs_path}/{status}_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"[LOG] Violation detected: {status} at {timestamp}")

    def start_monitoring(self):
        print("[DEBUG] Starting gaze monitoring...")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("[ERROR] Cannot access webcam.")
            return

        print("[INFO] Webcam accessed. Press 'q' to quit.")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("[ERROR] Failed to read from webcam.")
                break

            h, w = frame.shape[:2]
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.face_mesh.process(rgb)

            status = "Looking Forward"

            if result.multi_face_landmarks:
                for face_landmarks in result.multi_face_landmarks:
                    image_points = np.array([
                        (face_landmarks.landmark[1].x * w, face_landmarks.landmark[1].y * h),
                        (face_landmarks.landmark[152].x * w, face_landmarks.landmark[152].y * h),
                        (face_landmarks.landmark[263].x * w, face_landmarks.landmark[263].y * h),
                        (face_landmarks.landmark[33].x * w, face_landmarks.landmark[33].y * h),
                        (face_landmarks.landmark[287].x * w, face_landmarks.landmark[287].y * h),
                        (face_landmarks.landmark[57].x * w, face_landmarks.landmark[57].y * h)
                    ], dtype="double")

                    x_angle, y_angle, z_angle = self.get_head_pose(image_points, w, h)

                    if y_angle > 25:
                        status = "Looking Left"
                    elif y_angle < -25:
                        status = "Looking Right"
                    elif x_angle > 20:
                        status = "Looking Down"
                    elif x_angle < -20:
                        status = "Looking Up"

                    if status != "Looking Forward":
                        self.log_violation(frame, status)
                        cv2.putText(frame, f"WARNING: {status}", (30, 40),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    else:
                        cv2.putText(frame, "OK: Focused", (30, 40),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    self.mp_drawing.draw_landmarks(
                        frame,
                        face_landmarks,
                        self.mp_face_mesh.FACEMESH_TESSELATION,
                        self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                        self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1)
                    )

            cv2.imshow("Gaze Monitor", frame)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                print("[INFO] Quit key pressed.")
                break

        cap.release()
        cv2.destroyAllWindows()
        print("[INFO] Gaze monitoring stopped.")


if __name__ == "__main__":
    gaze = GazeMonitor()
    gaze.start_monitoring()
