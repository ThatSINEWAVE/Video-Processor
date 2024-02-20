import cv2
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip


def trim_audio_to_video(video_path, audio_path, output_path):
    print(f"Trimming audio: {audio_path} to match video: {video_path}")
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    video_length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    if fps != 0:
        video_length /= fps
    else:
        print(f"Error: FPS is 0 for video {video_path}, setting video length to 0")
        video_length = 0
    video.release()
    audio = AudioSegment.from_file(audio_path)
    audio = audio[25000:-25000]  # Trimming the first and last 25 seconds
    audio = audio - 10  # Reducing the volume by 10dB
    audio = audio[:int(video_length * 1000)]
    audio.export(output_path, format="wav")


def add_audio_to_video(video_path, audio_path, output_video_path):
    print(f"Adding audio: {audio_path} to video: {video_path}")
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac')
