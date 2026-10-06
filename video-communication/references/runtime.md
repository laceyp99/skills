# Renderer and media workflow

Read when generating an explanation from a different repository, setting up Manim, or using the narration and inspection helpers.

## Windows setup

Use Python 3.12, Manim 0.21.0, and Cairo. Reuse a compatible renderer outside worktrees; this skill supports Windows only.

Before the first render:

- Check `uv --version`. If unavailable, flag it and ask the user to set up [uv](https://docs.astral.sh/uv/getting-started/installation/).
- Check `ffmpeg -version` and `ffprobe -version`. If either is unavailable, ask the user to configure a Windows build from [FFmpeg's download page](https://ffmpeg.org/download.html) and expose its `bin` directory on PATH. These executables are required by our helpers.
- Check whether `ELEVEN_LABS_API_KEY` or a documented alias is configured, without displaying it. If absent, ask the user to configure an [ElevenLabs API key](https://elevenlabs.io/docs/api-reference/authentication) with text-to-speech access. Restart the agent or import a saved Windows variable as shown below. No SDK is required.

Report missing prerequisites and request setup; do not install tools or change PATH automatically. Continue independent scripting work while setup is pending.

The following PowerShell commands are setup instructions for a new renderer. Run them only when the user requests renderer setup:

```powershell
$rendererEnv = Join-Path $env:LOCALAPPDATA 'video-communication\manim-0.21.0'
uv python install 3.12
uv venv --python 3.12 "$rendererEnv"
$rendererPython = Join-Path $rendererEnv 'Scripts\python.exe'
uv pip install --python "$rendererPython" manim==0.21.0
& $rendererPython -m manim --version
ffmpeg -version
ffprobe -version
```

`<renderer-python>` below means this environment's `Scripts\python.exe`. Use it directly; shell activation and a `manim` entry on PATH are unnecessary. Reuse existing environments instead of recreating them.

If installation reports missing Microsoft Visual C++, flag the error and ask the user to follow [Manim's Windows build instructions](https://github.com/ManimCommunity/manim/blob/main/docs/source/installation/uv.md). Do not install build tools automatically.

Before spending speech credits, render a short preview using `Text` and native shapes to check fonts and rendering. Version output alone is insufficient. Native text and geometry do not need LaTeX; add it only for requested `Tex`/`MathTex` scenes. Choose installed fonts and record them. The prototype renderer occupied about 295 MiB, reused across worktrees.

## Job package

```text
<job>/
  storyboard.json
  scene.py
  sources.md
  audio/
  explanation.mp4
  captions.srt
  timeline.json
  validation.json
  contact-sheet.png
```

Choose a descriptive job name such as `murmur-pr-55`. Default local jobs to a machine artifact or temporary directory outside the source repository. Keep requested in-repository deliverables in that repository's documented artifacts/docs location. Preserve them for user review; temporary render caches can be separate.

`sources.md` records audience, inspected evidence and revision, hypothetical assumptions, generated asset provenance, voice/model, font and dependency versions, commands to reproduce, and unverified areas. Avoid copying private review notes wholesale into shareable artifacts.

The storyboard is JSON with a `cues` array of nonempty narration strings. Other metadata may describe the audience, source, scene intent, and destination. For example:

```json
{
  "pr_url": "https://github.com/owner/repo/pull/55",
  "head_sha": "inspected-full-commit-sha",
  "cues": [
    "Say I'm talking into a USB mic, but Windows still has the laptop mic selected.",
    "At the next stream start, the saved device is resolved again."
  ]
}
```

The scene remains authored for the material. Do not impose the prototype's six chapters or microphone assets on unrelated explanations.

## Narration

The helper uses Python's standard library and does not depend on a requests package:

```text
<renderer-python> <skill>/scripts/narrate.py <job>/storyboard.json --audio-dir <job>/audio
```

Override `--voice` and `--model` for established preferences. `--estimate` reports characters and cache misses without making network requests. Report characters or estimated credit use; look up current provider pricing if quoting money rather than hardcoding a rate.

The canonical key name is `ELEVEN_LABS_API_KEY`; aliases are `ELEVENLABS_API_KEY` and `ELEVEN_API_KEY`. The helper reads process variables only. A parent agent on Windows can import a saved variable without displaying it:

```powershell
if (-not $env:ELEVEN_LABS_API_KEY) {
    $env:ELEVEN_LABS_API_KEY = [Environment]::GetEnvironmentVariable('ELEVEN_LABS_API_KEY', 'User')
}
if (-not $env:ELEVEN_LABS_API_KEY) {
    $env:ELEVEN_LABS_API_KEY = [Environment]::GetEnvironmentVariable('ELEVEN_LABS_API_KEY', 'Machine')
}
```

Each clip has an MP3, normalized character alignment, and request fingerprint. Reuse is valid only when all are present and the fingerprint matches. Content-addressed entries live under `audio/cache/`; numbered files expose the active storyboard to the scene. A changed script or voice generates a new cache entry while preserving earlier successful clips. Exclude the cache directory from the shareable package.

A POST timeout, server failure, or interruption may have consumed credits. The helper leaves `pending.json` in that cache entry and blocks another request for it. Check provider history or recover the result before removing that marker; removing it permits another paid request. The helper does not automatically retry.

The initial prototype's legacy/library voice was unavailable through the free account's API, while premade voices worked. Recheck actual voice availability when a request fails; do not assume a subscription upgrade is needed for narration generally. Avoid printing raw HTTP bodies or headers.

## Scene timing and rendering

Resolve paths relative to the generated scene file, not the shell's working directory. Schedule audio with `Scene.add_sound` at each cue's start. Measure MP3 duration with ffprobe and wait for the clip to finish plus a small transition pause. Do not allow an animation to push narration into a different scene.

Use alignment's `characters`, `character_start_times_seconds`, and `character_end_times_seconds` for short caption phrases or precise visual events. Keep captions out of labels/code. Record actual rendered cue times in `timeline.json` as an array of `{ "index": 0, "start": 0.0, "end": 8.2, "text": "..." }`; use increasing nonoverlapping times. Emit standard SRT captions with actual speech timestamps.

Native shapes, `SVGMobject`, `ParametricFunction`, and `MoveAlongPath` cover icons, waveforms, and routed audio. Remove temporary animated objects by their actual scene members; removing only their original group can leave dots behind. When changing outline icon state, change stroke color rather than accidentally filling its interior and obscuring detail.

```text
<renderer-python> -m manim render -qm --fps 24 --disable_caching --media_dir <render-cache> -o explanation.mp4 <job>/scene.py <SceneClass>
```

Copy the completed MP4 from the output path reported by Manim into the job package. Do not guess that the command's working directory is the video's location. Use a lower-resolution preview only for iteration; identify its quality if delivering it instead of the requested output.

## Inspection

```text
<renderer-python> <skill>/scripts/inspect_video.py <job>/explanation.mp4 --timeline <job>/timeline.json --captions <job>/captions.srt --output <job>/validation.json --contact-sheet <job>/contact-sheet.png
```

The inspection helper uses ffmpeg/ffprobe. Contact sheets additionally use Pillow, already included in the Manim environment. It fails for broken media, missing narration tracks, silent audio, inconsistent track/scene duration, or invalid captions. It cannot judge factual correctness, visual semantics, pronunciations, or a human's comprehension. Inspect the generated frames and record that review separately in the validation notes.
