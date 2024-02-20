import subprocess


def generate_voice_narakeet():
    narakeet_api_key = "YOUR_NARAKEET_API_KEY"
    narakeet_repo_path = r"D:\Code\Video Pocessor Optimized\Narakeet-files"
    output_text = input("Enter the script text (or type 'quit' to exit):\n")

    if output_text.lower() == 'quit':
        return

    selected_voice = input("Select a voice (Alexandru/Alina):\n")
    audio_save_folder = r"D:\Code\Video Pocessor Optimized\Voice"

    narakeet_command = [
        "narakeet-api-client",
        "--api-key", narakeet_api_key,
        "--source", narakeet_repo_path,
        "--repository-type", "local-dir",
        "--repository", narakeet_repo_path,
        "--script", output_text,
        "--project-type", "audio",
        "--voice", selected_voice,
        "--output", audio_save_folder,
        "--verbose"
    ]

    result = subprocess.run(narakeet_command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print('Output:', result.stdout)
    print('Error:', result.stderr)


# Continuous input and generation loop
while True:
    generate_voice_narakeet()
