import cv2

from detection.camera import Camera
from detection.face_mesh import FaceMeshDetector
from detection.eye import EyeDetector
from detection.mouth import MouthDetector
from detection.head_pose import HeadPoseEstimator
from detection.blink import BlinkCounter
from detection.yawn import YawnCounter

from analysis.safety_score import SafetyScore
from analysis.distraction import DistractionDetector
from utils.smoother import ValueSmoother
from analysis.fatigue_analyzer import FatigueAnalyzer

from alerts.alarm import Alarm
from database.database_manager import DatabaseManager
from analysis.microsleep import MicrosleepDetector
from utils.event_logger import EventLogger
def main():

    camera = Camera()

    face_detector = FaceMeshDetector()

    eye_detector = EyeDetector()

    mouth_detector = MouthDetector()

    head_pose = HeadPoseEstimator()

    blink_counter = BlinkCounter()

    yawn_counter = YawnCounter()

    safety_score = SafetyScore()

    distraction_detector = DistractionDetector()

    alarm = Alarm()  

    fatigue_analyzer = FatigueAnalyzer()

    microsleep_detector = MicrosleepDetector()

    database = DatabaseManager()

    database.start_new_trip()

    event_logger = EventLogger()

    # -----------------------------
    # Head Pose Smoothers
    # -----------------------------
    pitch_smoother = ValueSmoother(window_size=10)
    yaw_smoother = ValueSmoother(window_size=10)
    roll_smoother = ValueSmoother(window_size=10)

    print("Press Q to Exit")

    while True:

        frame = camera.get_frame()

        if frame is None:
            break

        frame_height, frame_width = frame.shape[:2]

        face_detector.detect_landmarks(frame)

        face_landmarks = face_detector.get_face_landmarks()

        if face_landmarks:

            ###################################
            # Draw Face Mesh
            ###################################

            face_detector.draw_landmarks(frame)

            ###################################
            # EAR
            ###################################

            ear, left_eye, right_eye = eye_detector.get_average_ear(
                face_landmarks,
                frame_width,
                frame_height,
            )

            eye_detector.draw_eye_landmarks(
                frame,
                left_eye,
                right_eye,
            )

            ###################################
            # Blink Detection
            ###################################

            blink_detected = blink_counter.update(ear)

            ###################################
            # Microsleep Detection
            ###################################

            microsleep_detected = microsleep_detector.update(ear)

            ###################################
            # MAR
            ###################################

            mar = mouth_detector.calculate_mar(
                face_landmarks
            )

            ###################################
            # Yawn Detection
            ###################################

            yawn_detected = yawn_counter.update(mar)

            ###################################
            # Head Pose
            ###################################

            pitch, yaw, roll = head_pose.estimate_pose(
                face_landmarks,
                frame_width,
                frame_height,
            )

            ###################################
            # Smooth Head Pose
            ###################################

            pitch = pitch_smoother.update(pitch)
            yaw = yaw_smoother.update(yaw)
            roll = roll_smoother.update(roll)
            ###################################
            # Driver Direction
            ###################################

            direction, distracted = distraction_detector.update(
            yaw,
            pitch,
            )

            ###################################
            # Log Distraction
            ###################################

            if event_logger.has_changed(
            "Direction",
            direction,
            ):

                database.log_event(
                "Direction",
                direction,
                )
            

            ###################################
            # Fatigue Analyzer
            ###################################

            fatigue_analyzer.update(
            ear,
            distracted,
            ) 

            eye_closure = fatigue_analyzer.get_eye_closure()

            distraction = fatigue_analyzer.get_distraction()

            ###################################
            # Safety Score
            ###################################

            score = safety_score.calculate(
            eye_closure=eye_closure,
            distraction=distraction,
            ear=ear,
            mar=mar,
            microsleep=microsleep_detected,
            )

            status = safety_score.get_status()

            ###################################
            # Display Values
            ###################################

            cv2.putText(
                frame,
                f"EAR : {ear:.2f}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

            cv2.putText(
                frame,
                f"MAR : {mar:.2f}",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

            cv2.putText(
                frame,
                f"Pitch : {pitch:.1f}",
                (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2,
            )

            cv2.putText(
                frame,
                f"Yaw : {yaw:.1f}",
                (20, 145),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2,
            )

            cv2.putText(
                frame,
                f"Roll : {roll:.1f}",
                (20, 180),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2,
            )

            cv2.putText(
                frame,
                f"Blinks : {blink_counter.get_total_blinks()}",
                (20, 215),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2,
            )

            cv2.putText(
                frame,
                f"Yawns : {yawn_counter.get_total_yawns()}",
                (20, 250),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2,
            )
            ###################################
            # Driver Direction
            ###################################

            cv2.putText(
            frame,
            f"Direction : {direction}",
            (20, 360),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
            )

            driver_state = "DISTRACTED" if distracted else "ATTENTIVE"

            driver_color = (0, 0, 255) if distracted else (0, 255, 0)

            cv2.putText(
            frame,
            f"Driver : {driver_state}",
            (20, 395),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            driver_color,
            2,
            )

            ###################################
            # Fatigue Statistics
            ###################################

            cv2.putText(
            frame,
            f"Eye Closure : {eye_closure:.1f}%",
            (20, 430),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
            )

            cv2.putText(
            frame,
            f"Distraction : {distraction:.1f}%",
            (20, 465),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
            )

            ###################################
            # Safety Score Color
            ###################################

            if score >= 80:
                color = (0, 255, 0)

            elif score >= 60:
                color = (0, 255, 255)

            else:
                color = (0, 0, 255)

            cv2.putText(
                frame,
                f"Safety Score : {score}",
                (20, 285),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2,
            )

            cv2.putText(
                frame,
                f"Status : {status}",
                (20, 325),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2,
            )

            ###################################
            # Event-Based Warnings
            ###################################

            if blink_detected:
                database.log_event(
                    "Blink",
                    f"EAR={ear:.2f}"
                )
                cv2.putText(
                    frame,
                    "BLINK DETECTED",
                    (20, 500),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 165, 255),
                    2,
                )

            if yawn_detected:

                database.log_event(
                    "Yawn",
                    f"MAR={mar:.2f}"
                )
                cv2.putText(
                    frame,
                    "YAWNING DETECTED",
                    (20, 535),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2,
                )
            if microsleep_detected:

                cv2.putText(
                    frame,
                    "MICROSLEEP DETECTED!",
                    (20, 500),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    3,
                )
                if microsleep_detector.just_started():
                    database.log_event(
                        "Microsleep",
                        "Eyes Closed"
                    )
                alarm.start()
            else:
                alarm.stop()
        else:

            cv2.putText(
                frame,
                "No Face Detected",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
            )

        cv2.imshow("AI Driver Monitoring System", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    face_detector.close()
    camera.release()


if __name__ == "__main__":
    main()