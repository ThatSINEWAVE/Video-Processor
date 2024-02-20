import os
import random


def get_random_audio_file(music_folder):
    if music_folder == "Both":
        music_folder = random.choice(["TIKTOK_Music", "FACEBOOK_Music"])
    return os.path.join(f"Music/{music_folder}", random.choice(os.listdir(f"Music/{music_folder}")))
