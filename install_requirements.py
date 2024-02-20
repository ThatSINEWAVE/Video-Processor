import os
from setuptools import setup, find_packages

# Create necessary directories
directories = [
    "Music/FACEBOOK_Music",
    "Music/TIKTOK_Music",
    "Processed",
    "temp_clips/temp_facebook",
    "temp_clips/temp_tiktok",
    "Video/PLACEHOLDER/FACEBOOK_Videos",
    "Video/PLACEHOLDER/TIKTOK_Videos",
    "Watermark"
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)

# Setup script to install necessary packages
setup(
    name='video_processing_script',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python-headless==4.5.3',
        'pillow==8.3.1',
        'pydub==0.25.0',
        'moviepy==1.0.3',
        'scikit-image'
    ]
)
