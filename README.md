# Video Processor V1
The Video Processor V1 script emerged from a light-hearted debate about automation in the workplace, leading to the creation of a tool capable of automating aspects of ad production. Initially crafted as a jest, this script has evolved into a utility that others might find valuable for streamlining video ad creation processes.

## Introduction
This script automates several tasks involved in creating simple ads, including scene detection, clip cutting, and more. It's shared in the spirit of collaboration, inviting others to refine and expand its capabilities.

## Key Features
- Automated Scene Detection: Efficiently identifies and segments different scenes within a video.
- Random Music Selection: Chooses background music appropriate for platforms like TikTok and Facebook.
- Automated Watermarking: Adds watermarks to videos to protect and brand your content.
- Custom Video Duration: Sets the average runtime for the output videos according to your needs.
- Direct Logging to Telegram: Keeps a log of actions and updates in a designated Telegram channel.
- AI Voiceover: Incorporates voiceovers using the Narakeet API (Note: Currently non-operational).

## Technology Stack
- Audio Processing: Utilizes Pydub, cv2, and moviepy for comprehensive audio editing capabilities.
- Video Processing: Employs cv2, numpy, moviepy, and PIL for advanced video manipulation.
- Voice Processing: Integrates with the Narakeet API for generating voiceovers.
- Logging: Implements the Telegram Bot API for real-time logging and notifications.

## Getting Started
### Prerequisites
Ensure you have Python installed on your system and are familiar with package management using pip.

### Installation
- Clone the repository to your local machine.
- Install the required dependencies listed in requirements.txt using pip install -r requirements.txt.
- Launch main.py in your preferred IDE or from the command line.

### Usage Guide
Follow the on-screen prompts to configure the script:
- RAM Limit: Set the maximum RAM usage for the script (up to 12 GB recommended).
- Video Format Selection: Choose the output format tailored for Facebook, TikTok, or both.
- Watermark Options: Select from predefined watermark styles or opt for no watermark.
- Output Quantity: Determine the number of final videos to generate.
- Video Length: Specify the maximum length for each video in seconds.

## Contributing
Feel free to fork this repository and contribute by adding new features, fixing bugs, or improving the documentation. Your insights and contributions are highly valued.

## License
This project is open-sourced under the MIT License.
