"""
ARIS CLIP MOTION ENGINE
-----------------------
Creates motion clips from generated images.
Clips are stored in ARIS_OUTPUT/clips
"""

import os
import subprocess
from aris_paths import CLIP_PATH


class ARISClipMotionEngine:

    def __init__(self):

        self.output_folder = CLIP_PATH

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def create_motion_clip(self, image_path, duration, scene_id):

        output_video = os.path.join(self.output_folder, f"scene_{scene_id}.mp4")

        cmd = [
            "ffmpeg",
            "-y",
            "-loop", "1",
            "-i", image_path,
            "-c:v", "libx264",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            "-vf", "zoompan=z='min(zoom+0.0015,1.5)':d=125",
            output_video
        ]

        try:
            subprocess.run(cmd, check=True)
            return output_video
        except subprocess.CalledProcessError as e:
            print("ARIS CLIP ENGINE ERROR:", e)
            return None