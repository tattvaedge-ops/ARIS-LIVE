"""
ARIS VIDEO RENDER ENGINE
------------------------
Combines scene clips into final cinematic video.
Output stored in ARIS_OUTPUT/videos
"""

import os
import subprocess
from aris_paths import VIDEO_PATH


class ARISVideoRenderEngine:

    def __init__(self):

        self.output_folder = VIDEO_PATH

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def render_final_video(self, clips, output_name="aris_video.mp4"):

        concat_file = os.path.join(self.output_folder, "clips.txt")

        with open(concat_file, "w") as f:
            for clip in clips:
                f.write(f"file '{clip}'\n")

        output_path = os.path.join(self.output_folder, output_name)

        cmd = [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            output_path
        ]

        try:
            subprocess.run(cmd, check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            print("ARIS VIDEO RENDER ERROR:", e)
            return None