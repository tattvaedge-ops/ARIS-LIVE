import cv2
import os

from aris_cloud_video_client import generate_cloud_video


OUTPUT_FOLDER = "ARIS_OUTPUT"


def apply_ken_burns(image_path, duration=3, fps=24):

    img = cv2.imread(image_path)

    if img is None:
        print("Motion Engine: Failed to load image")
        return None

    h, w, _ = img.shape

    frames = []

    total_frames = duration * fps

    for i in range(total_frames):

        scale = 1 + (i / total_frames) * 0.15

        new_w = int(w * scale)
        new_h = int(h * scale)

        resized = cv2.resize(img, (new_w, new_h))

        x = (new_w - w) // 2
        y = (new_h - h) // 2

        crop = resized[y:y+h, x:x+w]

        frames.append(crop)

    return frames


def render_scene_video(scene_id, image_path, prompt=None):

    print(f"\nARIS MOTION ENGINE: Rendering scene {scene_id}")

    # -----------------------------
    # TRY CLOUD AI VIDEO
    # -----------------------------
    if prompt:

        print("Attempting AI video generation...")

        ai_video = generate_cloud_video(prompt, scene_id)

        if ai_video and os.path.exists(ai_video):

            print("AI video received")

            return ai_video

        else:

            print("AI video failed → using fallback motion")

    # -----------------------------
    # LOCAL FALLBACK MOTION
    # -----------------------------
    frames = apply_ken_burns(image_path)

    if frames is None:
        return None

    height, width, _ = frames[0].shape

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    video_path = os.path.join(OUTPUT_FOLDER, f"scene_{scene_id}.mp4")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    out = cv2.VideoWriter(video_path, fourcc, 24, (width, height))

    for frame in frames:
        out.write(frame)

    out.release()

    print("Local motion video created:", video_path)

    return video_path