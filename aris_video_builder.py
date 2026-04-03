import os

from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip

from aris_motion_engine import render_scene_video
from aris_timeline_engine import generate_scene_durations
from aris_film_director_engine import generate_edit_plan


def build_video(image_files, narration_file):

    print("\n==============================")
    print("ARIS VIDEO BUILDER STARTED")
    print("==============================\n")

    clips = []

    # -----------------------------
    # ENSURE OUTPUT DIRECTORY
    # -----------------------------
    os.makedirs("ARIS_OUTPUT", exist_ok=True)

    # -----------------------------
    # SAFETY CHECK
    # -----------------------------
    if not image_files:
        print("No images generated for video")
        return "No images generated"

    total_scenes = len(image_files)

    print("Total scenes:", total_scenes)

    # -----------------------------
    # GENERATE CINEMATIC PLANS
    # -----------------------------
    edit_plan = generate_edit_plan(total_scenes)

    scene_durations = generate_scene_durations(total_scenes)

    # -----------------------------
    # BUILD SCENE VIDEOS
    # -----------------------------
    scene_videos = []

    for i, img in enumerate(image_files):

        scene_id = i + 1

        print("\nProcessing Scene:", scene_id)

        # fallback duration if planner fails
        if i < len(scene_durations):
            duration = scene_durations[i]
        else:
            duration = 3

        # -----------------------------
        # GENERATE MOTION VIDEO
        # -----------------------------
        scene_video = render_scene_video(scene_id, img)

        if scene_video and os.path.exists(scene_video):

            clip = VideoFileClip(scene_video)

            # enforce planned duration
            clip = clip.with_duration(duration)

            scene_videos.append(clip)

        else:

            print("Motion render failed, falling back to image clip")

            clip = ImageClip(img).with_duration(duration)

            scene_videos.append(clip)

    # -----------------------------
    # CONCATENATE SCENES
    # -----------------------------
    print("\nCombining scenes...\n")

    video = concatenate_videoclips(scene_videos, method="compose")

    # -----------------------------
    # ADD NARRATION (OPTIONAL)
    # -----------------------------
    if narration_file and os.path.exists(narration_file):

        print("Adding narration:", narration_file)

        audio = AudioFileClip(narration_file)

        video = video.with_audio(audio)

    else:

        print("No narration file found, skipping audio")

    # -----------------------------
    # RENDER VIDEO
    # -----------------------------
    output_file = os.path.join("ARIS_OUTPUT", "aris_video_output.mp4")

    print("\nRendering final video...")

    video.write_videofile(output_file, fps=24)

    print("\nVideo created:", output_file)

    return output_file