import typer
from pathlib import Path
from typing import Optional
from midia_compress.utils.helper import list_mp4_files
from midia_compress.utils.video import check_ffmpeg, compress_video

app = typer.Typer(help="📹 Media Compressor - FFmpeg-based video compression tool")

def handle_missing_ffmpeg():
    """Show error message and exit if FFmpeg is missing"""
    typer.secho("❌ FFmpeg is not installed or not in PATH.", fg=typer.colors.RED, bold=True)
    typer.echo("Please install FFmpeg before continuing:")
    typer.secho("  Download: https://ffmpeg.org/download.html", fg=typer.colors.BLUE)
    raise typer.Exit(code=1)

def ask_directory() -> Path:
    """Prompt user for directory selection"""
    typer.echo("\n📂 Select working directory:")
    current_dir = Path.cwd()
    choice = typer.prompt(
        f"1. Current directory ({current_dir})\n"
        "2. Custom directory\n"
        "Enter choice (1/2)",
        type=int,
        show_choices=False
    )

    if choice == 1:
        return current_dir
    elif choice == 2:
        path = typer.prompt("Enter full directory path")
        return Path(path).expanduser().resolve()
    else:
        typer.secho("Invalid choice. Using current directory.", fg=typer.colors.YELLOW)
        return current_dir

def ask_compress_quality() -> int:
    """Prompt user for compression quality (CRF) with validation"""
    while True:
        crf = typer.prompt(
            "Enter compression quality (CRF 18-28)\n"
            "└── Lower values = better quality (23 is recommended)\n"
            "> ",
            default=23,
            type=int
        )

        if 18 <= crf <= 28:
            return crf
        typer.secho(
            "❌ Value must be between 18-28 (lower=better quality)",
            fg=typer.colors.RED
        )

@app.command()
def compress(
    crf: int = typer.Option(
        28,
        help="Compression Quality (18-28, where 23 is default)",
        min=18,
        max=28
    ),
    output_prefix: str = typer.Option(
        "compressed_",
        help="Prefix for output files"
    )
):
    """Compress all MP4 videos in directory"""
    # Verify FFmpeg
    if not check_ffmpeg():
        handle_missing_ffmpeg()

    # Select directory
    working_dir = ask_directory()
    typer.secho(f"\n🔍 Searching for MP4 files in: {working_dir}", fg=typer.colors.CYAN)

    # List files
    videos = list_mp4_files(working_dir)
    if not videos:
        typer.secho("No MP4 files found!", fg=typer.colors.YELLOW)
        raise typer.Exit()

    # Show files to process
    typer.echo("\n📹 Found videos:")
    for i, video in enumerate(videos, 1):
        typer.echo(f"  {i}. {video}")

    # Ask for compression quality
    crf = ask_compress_quality()

    # Process files
    with typer.progressbar(videos, label="Compressing") as progress:
        for video in progress:
            compress_video(
                str(video),
                crf=crf,
                force_overwrite=True
            )

    typer.secho("\n✅ All videos compressed successfully!", fg=typer.colors.GREEN, bold=True)

if __name__ == "__main__":
    app()