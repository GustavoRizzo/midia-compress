import imageio_ffmpeg

def check_ffmpeg() -> tuple[bool, str]:
    """
    Check if ffmpeg is installed internally on the system.
    Returns:
        tuple: A tuple containing a boolean indicating if ffmpeg is installed,
               and the path to the ffmpeg executable if it is installed.
    """
    try:
        path = imageio_ffmpeg.get_ffmpeg_exe()
        return (True, path)
    except Exception as e:
        return (False, None)