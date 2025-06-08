from midia_compress.utils.video import check_ffmpeg
def main():
    print("Starting midia_compress CLI...")
    has_ffmpeg, path = check_ffmpeg()
    print("Ending midia_compress CLI")


if __name__ == '__main__':
    main()