import os

# BASE OUTPUT DIRECTORY
BASE_OUTPUT = r"C:\AGENTIC AI- ARIS\ARIS_OUTPUT"

# OUTPUT DIRECTORIES
VIDEO_PATH = os.path.join(BASE_OUTPUT, "videos")
IMAGE_PATH = os.path.join(BASE_OUTPUT, "images")
CLIP_PATH = os.path.join(BASE_OUTPUT, "clips")
AUDIO_PATH = os.path.join(BASE_OUTPUT, "audio")
DOCUMENT_PATH = os.path.join(BASE_OUTPUT, "documents")
RESEARCH_PATH = os.path.join(BASE_OUTPUT, "research")


def ensure_folders():

    folders = [
        VIDEO_PATH,
        IMAGE_PATH,
        CLIP_PATH,
        AUDIO_PATH,
        DOCUMENT_PATH,
        RESEARCH_PATH
    ]

    for folder in folders:

        if not os.path.exists(folder):
            os.makedirs(folder)


# Automatically create folders
ensure_folders()    