from moviepy.audio.io.AudioFileClip import AudioFileClip


def generate_scene_durations(audio_file, total_scenes):

    audio = AudioFileClip(audio_file)

    total_duration = audio.duration

    scene_duration = total_duration / total_scenes

    durations = []

    for i in range(total_scenes):

        durations.append(scene_duration)

    print("TOTAL NARRATION LENGTH:", total_duration)
    print("SCENE DURATION:", scene_duration)

    return durations