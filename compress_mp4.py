"""Compress MP4 files with minimal or no quality impact using ffmpeg.

Examples:
    python compress_mp4.py "C:\\2026_AI_Collaboration\\Zoom\\25Feb.mp4"
    python compress_mp4.py "C:\\2026_AI_Collaboration\\Zoom\\25Feb.mp4" --mode lossless-copy
    python compress_mp4.py "C:\\2026_AI_Collaboration\\Zoom\\25Feb.mp4" \
            --mode visually-lossless --crf 18
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(command: list[str]) -> None:
    """Run a shell command and raise on failure."""
    process = subprocess.run(command, check=False)
    if process.returncode != 0:
        raise RuntimeError("ffmpeg command failed")


def file_size_mb(file_path: Path) -> float:
    """Return file size in MB."""
    return file_path.stat().st_size / (1024 * 1024)


def resolve_ffmpeg_binary() -> str:
    """Resolve ffmpeg binary from PATH or imageio-ffmpeg fallback."""
    ffmpeg_bin = shutil.which("ffmpeg")
    if ffmpeg_bin:
        return ffmpeg_bin

    try:
        from imageio_ffmpeg import get_ffmpeg_exe

        return get_ffmpeg_exe()
    except Exception as error:  # pragma: no cover
        raise RuntimeError(
            "ffmpeg is not installed or not in PATH. "
            "Install ffmpeg, or install Python package imageio-ffmpeg."
        ) from error


def build_output_path(input_path: Path, suffix: str) -> Path:
    """Create output file path next to the input file."""
    stem = input_path.stem
    output_name = f"{stem}_{suffix}.mp4"
    return input_path.with_name(output_name)


def compress_lossless_copy(input_path: Path, output_path: Path, ffmpeg_bin: str) -> None:
    """Copy streams without re-encoding to preserve exact quality."""
    command = [
        ffmpeg_bin,
        "-y",
        "-i",
        str(input_path),
        "-map_metadata",
        "-1",
        "-map_chapters",
        "-1",
        "-movflags",
        "+faststart",
        "-c",
        "copy",
        str(output_path),
    ]
    run_command(command)


def compress_visually_lossless(
    input_path: Path, output_path: Path, crf: int, ffmpeg_bin: str
) -> None:
    """Re-encode video for stronger compression with near-identical quality."""
    command = [
        ffmpeg_bin,
        "-y",
        "-i",
        str(input_path),
        "-map_metadata",
        "-1",
        "-map_chapters",
        "-1",
        "-c:v",
        "libx265",
        "-preset",
        "slow",
        "-crf",
        str(crf),
        "-tag:v",
        "hvc1",
        "-c:a",
        "copy",
        "-movflags",
        "+faststart",
        str(output_path),
    ]
    run_command(command)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Reduce MP4 size using ffmpeg. "
            "Use 'lossless-copy' for zero quality change, or 'visually-lossless' "
            "for stronger compression with near-identical quality."
        )
    )
    parser.add_argument("input_file", help="Path to the source MP4 file")
    parser.add_argument(
        "--mode",
        choices=["lossless-copy", "visually-lossless"],
        default="visually-lossless",
        help=(
            "Compression mode. "
            "lossless-copy keeps original streams (smaller gains), "
            "visually-lossless re-encodes video for larger gains."
        ),
    )
    parser.add_argument(
        "--crf",
        type=int,
        default=22,
        help="Starting CRF for visually-lossless mode (lower = larger/better). Typical: 20-28.",
    )
    parser.add_argument(
        "--max-crf",
        type=int,
        default=32,
        help="Maximum CRF to try when auto-increasing compression to ensure smaller output.",
    )
    parser.add_argument(
        "--no-ensure-smaller",
        action="store_true",
        help="Disable auto-retry logic that increases CRF until output is smaller than input.",
    )
    parser.add_argument(
        "--output",
        help="Optional output path. If omitted, creates <name>_<mode>.mp4 next to source.",
    )
    return parser.parse_args()


def main() -> int:
    """Entrypoint for MP4 compression workflow."""
    args = parse_args()
    input_path = Path(args.input_file).expanduser().resolve()

    if input_path.suffix.lower() != ".mp4":
        print("Input must be an .mp4 file")
        return 1

    if not input_path.exists():
        print(f"File not found: {input_path}")
        return 1

    try:
        ffmpeg_bin = resolve_ffmpeg_binary()
    except RuntimeError as error:
        print(error)
        return 1

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
    else:
        output_path = build_output_path(input_path, args.mode)

    if output_path == input_path:
        print("Output path must be different from input path")
        return 1

    if args.mode == "visually-lossless" and not 0 <= args.crf <= 51:
        print("CRF must be between 0 and 51")
        return 1

    if args.mode == "visually-lossless" and not 0 <= args.max_crf <= 51:
        print("max-crf must be between 0 and 51")
        return 1

    if args.mode == "visually-lossless" and args.max_crf < args.crf:
        print("max-crf must be greater than or equal to crf")
        return 1

    print(f"Input : {input_path}")
    print(f"Output: {output_path}")
    print(f"Mode  : {args.mode}")

    before_mb = file_size_mb(input_path)

    after_mb = before_mb

    try:
        if args.mode == "lossless-copy":
            compress_lossless_copy(input_path, output_path, ffmpeg_bin)
            after_mb = file_size_mb(output_path)
        else:
            current_crf = args.crf
            while True:
                print(f"\nEncoding with CRF {current_crf}...")
                compress_visually_lossless(input_path, output_path, current_crf, ffmpeg_bin)
                after_mb = file_size_mb(output_path)

                if args.no_ensure_smaller:
                    break

                if after_mb < before_mb:
                    break

                if current_crf >= args.max_crf:
                    break

                current_crf = min(current_crf + 2, args.max_crf)
                print(
                    "Output is not smaller yet; increasing CRF for stronger compression..."
                )
    except RuntimeError as error:
        print(f"Compression failed: {error}")
        return 1

    saved_mb = before_mb - after_mb
    saved_pct = (saved_mb / before_mb * 100) if before_mb > 0 else 0.0

    print(f"\nOriginal size : {before_mb:.2f} MB")
    print(f"Compressed size: {after_mb:.2f} MB")
    if saved_mb >= 0:
        print(f"Saved         : {saved_mb:.2f} MB ({saved_pct:.1f}%)")
    else:
        print(f"Size increased: {abs(saved_mb):.2f} MB ({abs(saved_pct):.1f}%)")
        if args.mode == "visually-lossless" and not args.no_ensure_smaller:
            print(
                "\nReached max CRF without getting smaller output. "
                "Try higher --max-crf or accept slight quality trade-off with higher CRF."
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
