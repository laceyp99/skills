"""Check rendered narration media and timing, optionally extracting scene frames."""

import argparse
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile


def run(command):
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return result.stdout + result.stderr


def check(condition, message):
    if not condition:
        raise ValueError(message)


def timestamp(value):
    hours, minutes, seconds, millis = map(int, re.split("[:,]", value))
    check(minutes < 60 and seconds < 60, "Invalid SRT timestamp")
    return hours * 3600 + minutes * 60 + seconds + millis / 1000


def inspect(args):
    metadata = json.loads(
        run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_streams",
                "-show_format",
                "-of",
                "json",
                str(args.video),
            ]
        )
    )
    duration = float(metadata["format"]["duration"])
    check(math.isfinite(duration) and duration > 0, "Invalid video duration")
    streams = metadata["streams"]
    check(any(s["codec_type"] == "video" for s in streams), "Missing video track")
    check(any(s["codec_type"] == "audio" for s in streams), "Missing narration track")
    for stream in streams:
        if stream["codec_type"] in ("audio", "video") and "duration" in stream:
            check(
                abs(float(stream["duration"]) - duration) < 0.5,
                "Track duration mismatch",
            )
    run(["ffmpeg", "-v", "error", "-xerror", "-i", str(args.video), "-f", "null", "-"])
    volume = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-i",
            str(args.video),
            "-vn",
            "-af",
            "volumedetect",
            "-f",
            "null",
            "-",
        ]
    )
    peak = re.search(r"max_volume: ([\-\w.]+) dB", volume)
    check(peak is not None, "Audio signal measurement unavailable")
    peak_db = float(peak.group(1))
    check(math.isfinite(peak_db) and peak_db > -60, "Silent or nearly silent narration")
    cues = json.loads(args.timeline.read_text(encoding="utf-8"))
    check(isinstance(cues, list) and bool(cues), "Empty cue timeline")
    last = 0.0
    for cue in cues:
        start, end = float(cue["start"]), float(cue["end"])
        check(
            math.isfinite(start)
            and math.isfinite(end)
            and last <= start < end <= duration + 0.1,
            "Invalid or overlapping cue timing",
        )
        last = end
    blocks = re.split(r"\n\s*\n", args.captions.read_text(encoding="utf-8-sig").strip())
    last = 0.0
    for index, block in enumerate(blocks, 1):
        lines = block.splitlines()
        check(
            len(lines) >= 3 and lines[0] == str(index),
            "Invalid SRT numbering or empty caption",
        )
        check(any(line.strip() for line in lines[2:]), "Empty caption text")
        match = re.fullmatch(
            r"(\d{2,}:\d{2}:\d{2},\d{3}) --> (\d{2,}:\d{2}:\d{2},\d{3})", lines[1]
        )
        check(match is not None, "Invalid SRT timing line")
        start, end = map(timestamp, match.groups())
        check(
            last <= start < end <= duration + 0.1,
            "Invalid or overlapping caption timing",
        )
        last = end
    if args.contact_sheet:
        from PIL import Image, ImageDraw

        sheet = Image.new("RGB", (960, math.ceil(len(cues) / 2) * 294), "#0b1220")
        draw = ImageDraw.Draw(sheet)
        with tempfile.TemporaryDirectory(prefix="video-inspection-") as temporary:
            for index, cue in enumerate(cues):
                moment = (cue["start"] + cue["end"]) / 2
                frame = Path(temporary) / f"{index}.png"
                run(
                    [
                        "ffmpeg",
                        "-v",
                        "error",
                        "-ss",
                        str(moment),
                        "-i",
                        str(args.video),
                        "-frames:v",
                        "1",
                        "-vf",
                        "scale=480:270",
                        str(frame),
                    ]
                )
                x, y = index % 2 * 480, index // 2 * 294
                with Image.open(frame) as picture:
                    sheet.paste(picture, (x, y))
                draw.text(
                    (x + 8, y + 274), f"Cue {index + 1} at {moment:.2f}s", fill="white"
                )
        sheet.save(args.contact_sheet)
    return {
        "mechanical_checks": "pass",
        "duration_seconds": duration,
        "peak_db": peak_db,
        "cue_count": len(cues),
        "caption_count": len(blocks),
        "visual_review": "pending",
        "listening_review": "pending",
        "source_accuracy_review": "pending",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--timeline", required=True, type=Path)
    parser.add_argument("--captions", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--contact-sheet", type=Path)
    args = parser.parse_args()
    try:
        result = inspect(args)
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        subprocess.CalledProcessError,
    ) as error:
        result = {"mechanical_checks": "fail", "reason": str(error)}
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result))
    if result["mechanical_checks"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
