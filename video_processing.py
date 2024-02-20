import cv2
from PIL import Image
import numpy as np
from moviepy.editor import ImageSequenceClip


def get_video_dimensions(video_path):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    aspect_ratio = width / height
    return (width, height), aspect_ratio


def calculate_new_dimensions(dimensions, aspect_ratio):
    width, height = dimensions
    if aspect_ratio > 1:  # Landscape
        new_height = int(width / aspect_ratio)
        new_dimensions = (width, new_height)
    elif aspect_ratio < 1:  # Portrait
        new_width = int(height * aspect_ratio)
        new_dimensions = (new_width, height)
    else:  # Square
        new_dimensions = dimensions
    return new_dimensions


def create_blurred_background(video_path, dimensions):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('temp_background.mp4', fourcc, 30, dimensions)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resizing and blurring
        frame = cv2.resize(frame, dimensions)
        frame = cv2.GaussianBlur(frame, (21, 21), 0)

        out.write(frame)

    cap.release()
    out.release()

    return 'temp_background.mp4'


def overlay_video_on_background(video_path, background_path, output_path, dimensions):
    cap = cv2.VideoCapture(video_path)
    cap_bg = cv2.VideoCapture(background_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 30, dimensions)

    while True:
        ret, frame = cap.read()
        ret_bg, frame_bg = cap_bg.read()

        if not ret or not ret_bg:
            break

        # Centering the original video on the blurred background
        height, width, _ = frame.shape
        bg_height, bg_width, _ = frame_bg.shape

        x_offset = (bg_width - width) // 2
        y_offset = (bg_height - height) // 2

        frame_bg[y_offset:y_offset + height, x_offset:x_offset + width] = frame

        out.write(frame_bg)

    cap.release()
    cap_bg.release()
    out.release()


def overlay_image_on_video(video_path, image_path, output_path, dimensions):
    print(f"Overlaying image: {image_path} on video: {video_path}")
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 30, dimensions)
    img_np = None
    if image_path:
        img = Image.open(image_path)
        img = img.resize(dimensions)
        img_np = np.array(img)
        if img_np.shape[2] == 4:
            img_np = img_np[:, :, :3]
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, dimensions)
        if image_path:
            frame = cv2.addWeighted(frame, 1, img_np, 1, 0)
        out.write(frame)
    cap.release()
    out.release()


def detect_scene_changes_and_get_clips(video_path, dimensions, fps):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    prev_frame = None
    scenes = []
    current_scene = []
    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, dimensions)
        if prev_frame is not None:
            diff = cv2.absdiff(frame, prev_frame)
            mean_diff = np.mean(diff)
            if mean_diff > 30:  # may need adjustment
                scenes.append(current_scene)
                current_scene = []
        current_scene.append(frame)
        prev_frame = frame
    if current_scene:
        scenes.append(current_scene)
    cap.release()
    clips = [ImageSequenceClip([cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in scene], fps=fps)
             for scene in scenes]
    return clips
