import os
import subprocess
import random
from datetime import datetime, timedelta

# Root directory for video editing
root_dir = r"D:\EDIT VIDEO"

# Ensure the directory exists
if not os.path.exists(root_dir):
    print(f"Directory {root_dir} does not exist.")
    exit(1)

# Change to the target directory
os.chdir(root_dir)

# Loop through each subdirectory
for subdir in os.listdir():
    subdir_path = os.path.join(root_dir, subdir)

    if os.path.isdir(subdir_path) and subdir.lower() != "background":
        # Create EDITED WATERMARK folder inside the subdirectory if not exists
        edited_folder = os.path.join(subdir_path, "EDITED WATERMARK")
        os.makedirs(edited_folder, exist_ok=True)

        # Process each video file in the subdirectory
        for ext in ("*.mp4", "*.webm"):
            for file in [f for f in os.listdir(subdir_path) if f.endswith(ext[1:])]:
                file_path = os.path.join(subdir_path, file)
                new_file_name = os.path.join(
                    edited_folder, f"IMG_{random.randint(1000, 9999)}.mp4"
                )

                # Randomized parameters
                bitrate = 10000 + random.randint(0, 1000)
                fps = 30
                contrast = 1.0 + random.random() * 0.1
                angle = random.randint(-1, 1)
                radians = angle * 3.14159 / 180

                # Generate a random creation date
                random_date = (
                    datetime.now() + timedelta(minutes=random.randint(0, 15))
                ).strftime("%Y-%m-%dT%H:%M:%S")

                # Get video duration using ffmpeg
                try:
                    result = subprocess.run(
                        [
                            "ffmpeg",
                            "-i",
                            file_path,
                        ],
                        stderr=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        text=True,
                    )
                    duration_line = [
                        line for line in result.stderr.split("\n") if "Duration" in line
                    ][0]
                    duration = duration_line.split(",")[0].split()[1]
                    hours, minutes, seconds = map(float, duration.split(":"))
                    total_seconds = int(hours * 3600 + minutes * 60 + seconds)
                except Exception as e:
                    print(f"Error retrieving duration for {file_path}: {e}")
                    continue

                # Construct and execute the ffmpeg command
                ffmpeg_command = [
                    "ffmpeg",
                    "-i",
                    file_path,
                    "-stream_loop",
                    "-1",
                    "-i",
                    "runningtext.gif",
                    "-filter_complex",
                    f"[0:v]scale=1080:-1, crop=1080:1920, eq=contrast={contrast}, rotate={radians}[scaled]; [scaled]overlay=(main_w-overlay_w)/2:80[outv]",
                    "-map",
                    "[outv]",
                    "-map",
                    "0:a",
                    "-c:v",
                    "h264_nvenc",
                    "-b:v",
                    f"{bitrate}k",
                    "-metadata",
                    f"creation_time={random_date}",
                    "-metadata:s:a:0",
                    "language=eng",
                    "-metadata",
                    "encoder=Lavf60.3.100",
                    "-t",
                    str(total_seconds),
                    "-y",
                    new_file_name,
                ]

                try:
                    subprocess.run(ffmpeg_command, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error processing file {file_path}: {e}")
                    continue

                # Check if the output file exists and is not 0KB
                if os.path.exists(new_file_name):
                    if os.path.getsize(new_file_name) == 0:
                        print(f"Deleting empty file: {new_file_name}")
                        os.remove(new_file_name)

print("All videos have been modified and moved to the respective EDITED folders.")
