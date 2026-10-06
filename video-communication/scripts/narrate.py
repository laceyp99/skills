"""Generate timestamped ElevenLabs clips with a content-addressed local cache."""

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import shutil
import urllib.error
import urllib.parse
import urllib.request


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def valid_cache(folder, fingerprint):
    try:
        alignment = read_json(folder / "alignment.json")
        return (
            (folder / "audio.mp3").stat().st_size > 0
            and read_json(folder / "request.json")["fingerprint"] == fingerprint
            and len(alignment["characters"]) > 0
            and len(alignment["characters"])
            == len(alignment["character_start_times_seconds"])
            == len(alignment["character_end_times_seconds"])
        )
    except (OSError, ValueError, KeyError, TypeError):
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("storyboard", type=Path)
    parser.add_argument("--audio-dir", required=True, type=Path)
    parser.add_argument("--voice", default="cjVigY5qzO86Huf0OWal")
    parser.add_argument("--model", default="eleven_flash_v2_5")
    parser.add_argument("--estimate", action="store_true")
    args = parser.parse_args()
    cues = read_json(args.storyboard)["cues"]
    if (
        not isinstance(cues, list)
        or not cues
        or any(not isinstance(cue, str) or not cue.strip() for cue in cues)
    ):
        parser.error("cues must be a nonempty list of nonempty narration strings")
    jobs = []
    for index, cue in enumerate(cues):
        payload = {"text": cue, "model_id": args.model}
        fingerprint = hashlib.sha256(
            json.dumps([args.voice, payload], sort_keys=True).encode("utf-8")
        ).hexdigest()
        folder = args.audio_dir / "cache" / fingerprint
        jobs.append((index, payload, fingerprint, folder))
    missing = {
        fp: payload for _, payload, fp, folder in jobs if not valid_cache(folder, fp)
    }
    print(
        json.dumps(
            {
                "characters": sum(map(len, cues)),
                "uncached_characters": sum(
                    len(payload["text"]) for payload in missing.values()
                ),
                "uncached_requests": len(missing),
                "voice": args.voice,
                "model": args.model,
            }
        )
    )
    if args.estimate:
        return
    key = next(
        (
            os.environ[name]
            for name in ("ELEVEN_LABS_API_KEY", "ELEVENLABS_API_KEY", "ELEVEN_API_KEY")
            if os.environ.get(name)
        ),
        None,
    )
    if missing and not key:
        raise SystemExit("Set ELEVEN_LABS_API_KEY in the process environment first.")
    for index, payload, fingerprint, folder in jobs:
        if not valid_cache(folder, fingerprint):
            # A pending marker survives timeouts or interruption. Never rebill silently.
            folder.mkdir(parents=True, exist_ok=True)
            pending = folder / "pending.json"
            if pending.exists():
                raise SystemExit(
                    f"Uncertain previous request in {folder}. Check provider history before removing pending.json."
                )
            pending.write_text(
                json.dumps({"fingerprint": fingerprint}), encoding="utf-8"
            )
            request = urllib.request.Request(
                "https://api.elevenlabs.io/v1/text-to-speech/"
                + urllib.parse.quote(args.voice, safe="")
                + "/with-timestamps",
                data=json.dumps(payload).encode("utf-8"),
                headers={"xi-api-key": key, "Content-Type": "application/json"},
                method="POST",
            )
            try:
                with urllib.request.urlopen(request, timeout=90) as response:
                    result = json.load(response)
                audio = base64.b64decode(result["audio_base64"], validate=True)
                alignment = result.get("normalized_alignment") or result["alignment"]
                (folder / "audio.mp3").write_bytes(audio)
                (folder / "alignment.json").write_text(
                    json.dumps(alignment), encoding="utf-8"
                )
                (folder / "request.json").write_text(
                    json.dumps({"fingerprint": fingerprint}), encoding="utf-8"
                )
                if not valid_cache(folder, fingerprint):
                    raise ValueError("Incomplete audio or character alignment")
                pending.unlink()
            except urllib.error.HTTPError as error:
                # Status alone is useful and cannot leak provider response data.
                if error.code < 500:
                    pending.unlink()
                raise SystemExit(
                    f"ElevenLabs HTTP {error.code}. Generation stopped; cached clips preserved."
                    + (
                        " Completion uncertain; check provider history before retrying."
                        if error.code >= 500
                        else ""
                    )
                ) from None
            except (OSError, ValueError, KeyError) as error:
                raise SystemExit(
                    f"Request completion uncertain ({type(error).__name__}). Check provider history; no automatic retry."
                ) from None
        args.audio_dir.mkdir(parents=True, exist_ok=True)
        for source, suffix in (
            ("audio.mp3", ".mp3"),
            ("alignment.json", ".alignment.json"),
            ("request.json", ".request.json"),
        ):
            shutil.copyfile(folder / source, args.audio_dir / f"{index:02}{suffix}")
        print(f"Ready {index:02}.mp3")
    (args.audio_dir / "provider.json").write_text(
        json.dumps(
            {"provider": "ElevenLabs", "voice": args.voice, "model": args.model}
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
