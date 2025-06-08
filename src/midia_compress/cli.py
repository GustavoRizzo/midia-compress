
from midia_compress.utils.helper import list_mp4_files
from midia_compress.utils.video import check_ffmpeg, compress_video


def handle_not_have_ffmpeg():
    print("FFmpeg is not installed or not in PATH.")
    print("Please install FFmpeg before continuing.")
    print("Download: https://ffmpeg.org/download.html")
    exit(1)  # Exit script with error code

def main():
    print("Starting midia_compress CLI...")
    if not check_ffmpeg():
        handle_not_have_ffmpeg()
    list_mp4_files()
    for video in list_mp4_files():
        print(f"Processing video: {video}")
        compress_video(video, f"compressed_{video}", crf=28)
    print("Ending midia_compress CLI")


if __name__ == '__main__':
    main()