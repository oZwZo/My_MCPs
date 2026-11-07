#!/usr/bin/env python3
"""Turn a spoken script into an MP3 with Kokoro.

A blank line in the script marks a section break, which gets a longer pause.

Usage: tts.py SCRIPT.txt OUTPUT.mp3 [--voice af_heart] [--speed 0.88]
"""
import argparse
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

import numpy as np
import onnxruntime as ort
import soundfile as sf
from kokoro_onnx import Kokoro
from kokoro_onnx.config import EspeakConfig

ENGINE_DIR = Path.home() / ".local/share/speak"
SYSTEM_ESPEAK_LIB = Path("/usr/lib64/libespeak-ng.so.1")
SYSTEM_ESPEAK_DATA = Path("/usr/share/espeak-ng-data")


def load_engine() -> Kokoro:
    options = ort.SessionOptions()
    # sched_getaffinity respects a Slurm allocation, but macOS does not have it.
    if hasattr(os, "sched_getaffinity"):
        options.intra_op_num_threads = len(os.sched_getaffinity(0))
    else:
        options.intra_op_num_threads = os.cpu_count() or 1
    options.inter_op_num_threads = 1
    session = ort.InferenceSession(
        str(ENGINE_DIR / "model/kokoro-v1.0.onnx"),
        sess_options=options,
        providers=["CPUExecutionProvider"],
    )
    # The espeak library bundled with kokoro-onnx needs glibc 2.29, which this
    # cluster does not have, and its data files do not match the system library.
    config = None
    if SYSTEM_ESPEAK_LIB.exists() and SYSTEM_ESPEAK_DATA.exists():
        config = EspeakConfig(lib_path=str(SYSTEM_ESPEAK_LIB), data_path=str(SYSTEM_ESPEAK_DATA))
    return Kokoro.from_session(session, str(ENGINE_DIR / "model/voices-v1.0.bin"), espeak_config=config)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--voice", default="af_heart")
    parser.add_argument("--lang", default="en-us")
    parser.add_argument("--speed", type=float, default=0.88)
    parser.add_argument("--sentence-pause", type=float, default=0.45)
    parser.add_argument("--clause-pause", type=float, default=0.15)
    parser.add_argument("--section-pause", type=float, default=1.0)
    parser.add_argument("--bitrate", type=int, default=96)
    args = parser.parse_args()

    sections = [s.strip() for s in args.script.read_text().split("\n\n") if s.strip()]
    if not sections:
        raise SystemExit(f"No text in {args.script}")

    engine = load_engine()
    start = time.time()
    parts = []
    rate = None
    for section in sections:
        samples, rate = engine.create(
            section,
            voice=args.voice,
            speed=args.speed,
            lang=args.lang,
            sentence_pause=args.sentence_pause,
            clause_pause=args.clause_pause,
        )
        parts.append(samples)
        parts.append(np.zeros(int(args.section_pause * rate), dtype=samples.dtype))
    audio = np.concatenate(parts[:-1])

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=args.output.parent) as tmp:
        wav = Path(tmp) / "speech.wav"
        sf.write(wav, audio, rate)
        subprocess.run(["sox", str(wav), "-C", str(args.bitrate), str(args.output)], check=True)

    print(json.dumps({
        "mp3": str(args.output),
        "audio_seconds": round(len(audio) / rate, 1),
        "generation_seconds": round(time.time() - start, 1),
        "sections": len(sections),
        "words": len(args.script.read_text().split()),
        "voice": args.voice,
        "speed": args.speed,
    }))


if __name__ == "__main__":
    main()
