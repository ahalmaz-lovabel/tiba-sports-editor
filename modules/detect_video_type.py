"""
Video Type Detection Module
كشف نوع الفيديو

Uses MediaPipe to detect:
- Speaker/Presenter: Person speaking to camera
- Sports Action: Athletic activities and movements
"""

import cv2
import mediapipe as mp
from pathlib import Path


class VideoTypeDetector:
    """Detect video content type using MediaPipe"""

    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_face = mp.solutions.face_detection
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True
        )
        self.face_detector = self.mp_face.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.5
        )

    def detect(self, video_path: str, sample_frames: int = 10) -> str:
        """
        Detect video type by analyzing key frames

        Args:
            video_path: Path to video file
            sample_frames: Number of frames to analyze

        Returns:
            "speaker" or "sports"
        """
        video_path = Path(video_path)

        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        cap = cv2.VideoCapture(str(video_path))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Sample frames evenly throughout video
        frame_indices = [
            int(i * total_frames / sample_frames)
            for i in range(sample_frames)
        ]

        speaker_score = 0
        sports_score = 0

        for frame_idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()

            if not ret:
                continue

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect face
            face_results = self.face_detector.process(frame_rgb)
            has_face = face_results.detections is not None and len(face_results.detections) > 0

            # Detect pose
            pose_results = self.pose.process(frame_rgb)
            has_pose = pose_results.pose_landmarks is not None

            # Analyze pose for movement intensity
            movement_score = 0
            if has_pose:
                movement_score = self._calculate_movement_intensity(
                    pose_results.pose_landmarks
                )

            # Score assignment
            if has_face and movement_score < 0.3:
                speaker_score += 1  # Face-focused, minimal movement
            elif movement_score > 0.5:
                sports_score += 1  # High movement

        cap.release()
        self.face_detector.close()
        self.pose.close()

        # Determine type
        if sports_score > speaker_score:
            return "sports"
        else:
            return "speaker"

    def _calculate_movement_intensity(self, landmarks) -> float:
        """Calculate movement intensity from pose landmarks"""
        if not landmarks or len(landmarks) < 15:
            return 0.0

        # Focus on key joints for movement
        key_joints = [15, 16, 17, 18, 19, 20]  # Arms and hands

        movement = 0.0
        for joint_idx in key_joints:
            if joint_idx < len(landmarks):
                landmark = landmarks[joint_idx]
                # Movement based on confidence and visibility
                if landmark.visibility > 0.5:
                    movement += landmark.visibility

        return movement / len(key_joints)
