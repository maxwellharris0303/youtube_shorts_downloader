import os
import random
import subprocess
from datetime import datetime, timedelta
from time import sleep
import threading
import ffmpeg

lock = threading.Lock()

def run_command(cmd, directory):
    process = subprocess.Popen(cmd, shell=True, cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.pid

def run_command_1(command):
    """Run an ADB command using subprocess."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error running command: {command}\n{stderr.decode('utf-8')}")
    # else:
    #     print(f"Successfully ran command: {command}")
    return stdout.decode('utf-8')

def get_cmd_pid():
    parts = run_command_1(f'tasklist /FI "IMAGENAME eq cmd.exe"').split()
    # Find the last occurrence of 'cmd.exe'
    last_index = len(parts) - 1 - parts[::-1].index('cmd.exe')

    # Get the PID (it's right after 'cmd.exe')
    last_cmd_pid = parts[last_index + 1]

    # print(f"The last 'cmd.exe' PID is: {last_cmd_pid}")
    return last_cmd_pid

# Loop through each subfolder
# for folder in os.listdir(MAIN_DIR):
def run_thread(main_dir, folder_name, index):
    folder_path = os.path.join(main_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    if os.path.isdir(folder_path) and folder_name != "background":

 
        # Create the "EDITED WATERMARK" folder if it doesn't exist
        edited_folder = os.path.join(folder_path, "EDITED WATERMARK")
        os.makedirs(edited_folder, exist_ok=True)

        # Define the path to the promo video
        promo_path = "promo.mp4"

        # Process each video file (MP4 and WEBM) in the subfolder
        while True:
            # sleep(10)
            sleep(5)
            if len(os.listdir(folder_path)) < 2:
                break

            for file_name in os.listdir(folder_path):
                if file_name.endswith((".mp4", ".webm")):
                    try:
                        file_path = os.path.join(folder_path, file_name)
                        random_file_name = f"IMG_{random.randint(1000, 9999)}.mp4"
                        new_file_path = os.path.join(folder_path, random_file_name)
                        final_file_path = os.path.join(edited_folder, random_file_name)
                        
                        # Set random video properties
                        bitrate = 10000 + random.randint(0, 1000)
                        fps = 30
                        contrast = f"1.{random.randint(0, 9)}"
                        angle = random.randint(-1, 1)
                        radians = angle * 3.14 / 180

                        # Generate a random creation date within the last 15 minutes
                        random_date = (datetime.now() - timedelta(minutes=random.randint(0, 15))).strftime('%Y-%m-%dT%H:%M:%S')
                        
                        # Get the duration of the video in seconds
                        ffmpeg_command = f'ffmpeg -i "{file_path}" 2>&1'
                        result = subprocess.run(ffmpeg_command, shell=True, capture_output=True, text=True)
                        duration_line = next((line for line in result.stdout.splitlines() if "Duration" in line), None)
                        
                        if duration_line:
                            duration_str = duration_line.split(",")[0].split("Duration:")[1].strip()
                            hours, minutes, seconds = map(float, duration_str.split(":"))
                            total_seconds = int(hours * 3600 + minutes * 60 + seconds)

                            # Run ffmpeg command to process video
                            ffmpeg_command = [
                                "ffmpeg", "-i", file_path,
                                "-stream_loop", "-1", "-i", "runningtext.gif",
                                "-filter_complex",
                                f"[0:v]scale=1080:-1, crop=1080:1920, eq=contrast={contrast}, rotate={radians}[scaled]; [scaled]overlay=(main_w-overlay_w)/2:80[outv]",
                                "-map", "[outv]", "-map", "0:a",
                                "-c:v", "h264_nvenc",
                                f"-b:v", f"{bitrate}k",
                                "-metadata", f"creation_time={random_date}",
                                "-metadata:s:a:0", "language=eng",
                                "-metadata", "encoder=Lavf60.3.100",
                                "-t", str(total_seconds),
                                "-y", new_file_path
                            ]
                            subprocess.run(ffmpeg_command)

                            while True:
                                if os.path.exists(new_file_path) and os.path.getsize(new_file_path) > 0:
                                    break
                                sleep(1)

                            if os.path.exists(new_file_path) and os.path.getsize(new_file_path) > 0:
                                def concatenate_videos_reencode(input1, input2, output):
                                    # Re-encode videos to ensure compatibility, then concatenate
                                    temp1 = f"temp{index}.ts"
                                    temp2 = f"temp{index}0.ts"

                                    # Convert input videos to MPEG-TS format
                                    ffmpeg.input(input1).output(temp1, format="mpegts", vcodec="libx264", acodec="aac").run()
                                    ffmpeg.input(input2).output(temp2, format="mpegts", vcodec="libx264", acodec="aac").run()

                                    # Concatenate the .ts files
                                    ffmpeg.input(f"concat:{temp1}|{temp2}", format="mpegts").output(output, vcodec="copy", acodec="copy").run()

                                    print(f"Concatenated video saved as {output}")

                                    os.remove(temp1)
                                    os.remove(temp2)

                                # Example usage
                                concatenate_videos_reencode(new_file_path, "promo.mp4", final_file_path)

                                # Cleanup intermediate files
                                if os.path.exists(final_file_path) and os.path.getsize(final_file_path) > 0:
                                    os.remove(new_file_path)
                            else:
                                print(f"Deleting empty file: {new_file_path}")
                                os.remove(new_file_path)
                            if os.path.exists(file_path) and os.path.getsize(file_path) != 0:
                                print(f"Deleting origin file: {file_path}")
                                os.remove(file_path)
                    except:
                        if os.path.exists(file_path) and os.path.getsize(file_path) != 0:
                                print(f"Deleting origin file: {file_path}")
                                os.remove(file_path)

    return "success"


                    

