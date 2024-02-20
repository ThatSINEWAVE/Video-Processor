
# Video Processor V1

Video Processor script that automates simple AD making. This script became a thing while debating with employees if a script could automate their jobs and i wrote it like a joke ( it really was a joke )

Decided to post it publicly with the idea that maybe someone finds it useful and polishes it more making it into a complete app.


## Features

- Automated scene detection and cutting clips
- Random music selector based on platform ( Tiktok / Facebook / Both )
- Automated watermark
- Ability to set the average run time of videos
- Logging actions directly to telegram channels
- AI Voiceover using Narakeet ( Broken ATM )


## Tech Used

**Audio Processing:** Pydub, cv2, moviepy

**Video Processing:** cv2, numpy, moviepy, PIL

**Voice Processing:** Narakeet API

**Logs:** Telegram Bot API
## Deployment

To run the script install every package inside requirements.txt and run main.py in your favorite IDE

From there the script will guide you through the steps shown below:

1. Enter the maximum RAM limit in GB:
( Max: 12 GB )

2. Choose video format:
- 1 - Facebook
- 2 - Tiktok
- 3 - Both

3. Choose watermark options:
- no watermark
- oricare
- reducerino
- all

4. Enter the number of final videos to create: 
( Type the number of videos you want )

5. Enter the maximum video length in seconds: 
( Type the max video length you wish)

## License

[MIT](https://choosealicense.com/licenses/mit/)

