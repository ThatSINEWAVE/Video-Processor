import os
import shutil
import random
import cv2
from moviepy.editor import VideoFileClip, concatenate_videoclips
from telegram_logger import send_telegram_message
from video_processing import (get_video_dimensions, calculate_new_dimensions,
                              overlay_image_on_video, detect_scene_changes_and_get_clips,
                              create_blurred_background, overlay_video_on_background)
from audio_processing import trim_audio_to_video, add_audio_to_video
from file_management import get_random_audio_file


# Override the print function
def custom_print(*args, **kwargs):
    original_print(*args, **kwargs)
    message = " ".join(map(str, args))
    send_telegram_message(message)


original_print = print
print = custom_print


def process_videos():
    user_ram_limit_gb = float(input("Enter the maximum RAM limit in GB:\n( Max: 12 GB )"))
    format_choice = int(input("Choose video format:\n1 - Facebook\n2 - Tiktok\n3 - Both\n").strip())
    watermark_choice = int(input("Choose watermark options:\n1 - no watermark\n2 - oricare\n3 - reducerino\n4 - all\n")
                           .strip())
    number_of_videos = int(input("Enter the number of final videos to create: ").strip())
    max_video_length = int(input("Enter the maximum video length in seconds: ").strip()) * 60
    temp_clip_dir = "temp_clips"
    temp_facebook_dir = os.path.join(temp_clip_dir, "temp_facebook")
    temp_tiktok_dir = os.path.join(temp_clip_dir, "temp_tiktok")
    shutil.rmtree(temp_clip_dir, ignore_errors=True)
    os.makedirs(temp_facebook_dir)
    os.makedirs(temp_tiktok_dir)
    clip_paths = []
    watermark_paths = [None, "Overlay/oricare.png", "Overlay/reducerino.png"]

    dimensions = (0, 0)  # Assign a default value to dimensions here

    for root, dirs, files in os.walk("Video"):
        print(f"Checking in directory: {root}")
        for dir in dirs:
            if dir in ["TIKTOK_Videos", "FACEBOOK_Videos"]:
                current_folder = os.path.join(root, dir)
                print(f"Found video folder: {current_folder}")
                first_file = next((f for f in os.listdir(current_folder) if f.endswith(".mp4")), None)
                if first_file:
                    video_file_path = os.path.join(current_folder, first_file)
                    dimensions, aspect_ratio = get_video_dimensions(video_file_path)
                    dimensions = calculate_new_dimensions(dimensions, aspect_ratio)
                    cap = cv2.VideoCapture(video_file_path)
                    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30  # Defined the fps here
                    cap.release()
                else:
                    print(f"No video files found in {current_folder}, skipping...")
                    continue
                for file in os.listdir(current_folder):
                    if file.endswith(".mp4"):
                        video_file_path = os.path.join(current_folder, file)

                        # Check if the video is not in the correct format
                        is_facebook = "FACEBOOK_Videos" in current_folder
                        desired_aspect_ratio = 1 if is_facebook else 9 / 16
                        current_aspect_ratio = dimensions[0] / dimensions[1]

                        if current_aspect_ratio != desired_aspect_ratio:
                            background_video_path = create_blurred_background(video_file_path, dimensions)
                            formatted_video_path = f"formatted_{file}"
                            overlay_video_on_background(video_file_path, background_video_path, formatted_video_path,
                                                        dimensions)
                            video_file_path = formatted_video_path  # Update video_file_path to use the formatted video

                        scene_clips = detect_scene_changes_and_get_clips(video_file_path, dimensions, fps)
                        print(f"Processing video: {video_file_path}")
                        if "TIKTOK_Videos" in current_folder:
                            clip_temp_dir = temp_tiktok_dir
                        else:
                            clip_temp_dir = temp_facebook_dir
                        for clip_index, clip in enumerate(scene_clips):
                            temp_clip_path = os.path.join(clip_temp_dir, f"temp_clip_{clip_index}.mp4")
                            clip.write_videofile(temp_clip_path, codec='libx264', audio_codec='aac', fps=fps,
                                                 ffmpeg_params=['-profile:v', 'baseline', '-level', '3.0', '-pix_fmt',
                                                                'yuv420p'])
                            clip_paths.append(temp_clip_path)
                            del clip
    clips = [VideoFileClip(path) for path in clip_paths]
    for i in range(number_of_videos):
        random.shuffle(clips)
        selected_clips = []
        total_duration = 0
        for clip in clips:
            if total_duration + clip.duration <= max_video_length:
                total_duration += clip.duration
                selected_clips.append(clip)
            else:
                break
        final_clip = concatenate_videoclips(selected_clips, method="compose")
        output_video_path = f"Output/video_{i}.mp4"
        final_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac')

        music_folder = "Both" if format_choice == 3 else "FACEBOOK_Music" if format_choice == 1 else "TIKTOK_Music"
        audio_file = get_random_audio_file(music_folder)
        output_audio_path = f"Output/audio_{i}.wav"
        trim_audio_to_video(output_video_path, audio_file, output_audio_path)
        if watermark_choice == 4:
            watermark_paths_iteration = [None, "Overlay/oricare.png", "Overlay/reducerino.png"]
        else:
            watermark_paths_iteration = [random.choice(watermark_paths)]
        for watermark_index, watermark_image in enumerate(watermark_paths_iteration):
            final_output_video_path = f"Output/final_video_{i}_{watermark_index}.mp4"
            overlay_image_on_video(output_video_path, watermark_image, final_output_video_path, dimensions)

            # Adding audio to the video
            add_audio_to_video(final_output_video_path, output_audio_path,
                               f"Output/complete_video_{i}_{watermark_index}.mp4")

            # Clean up
            os.remove(final_output_video_path)

        # Clean up
        os.remove(output_video_path)
        os.remove(output_audio_path)


if __name__ == "__main__":
    process_videos()
