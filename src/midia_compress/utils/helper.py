import os


def list_mp4_files():
    """
    List all .mp4 files in the current directory.
    """
    mp4_files = [f for f in os.listdir('.') if f.endswith('.mp4') and os.path.isfile(f)]
    print("MP4 files in the current directory:", mp4_files)
    return mp4_files
