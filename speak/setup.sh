#!/usr/bin/env bash
# Install the speech engine and the speak skill. Safe to run more than once.
set -euo pipefail

SKILL_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DST="$HOME/.claude/skills/speak"
ENGINE="$HOME/.local/share/speak"
MODEL_URL="https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0"

for tool in uv sox espeak-ng; do
    command -v "$tool" >/dev/null || { echo "Missing required tool: $tool" >&2; exit 1; }
done

mkdir -p "$ENGINE/model"
[ -x "$ENGINE/venv/bin/python" ] || uv venv -q --python 3.11 "$ENGINE/venv"
uv pip install -q --python "$ENGINE/venv/bin/python" "kokoro-onnx==0.6.1" soundfile

for file in kokoro-v1.0.onnx voices-v1.0.bin; do
    if [ ! -s "$ENGINE/model/$file" ]; then
        echo "Downloading $file"
        curl -fL --retry 3 -o "$ENGINE/model/$file.part" "$MODEL_URL/$file"
        mv "$ENGINE/model/$file.part" "$ENGINE/model/$file"
    fi
done

if [ -e "$SKILL_DST" ]; then
    echo "Skill already exists at $SKILL_DST, so it was left unchanged."
else
    mkdir -p "$(dirname "$SKILL_DST")"
    cp -R "$SKILL_SRC" "$SKILL_DST"
    echo "Installed the skill at $SKILL_DST"
fi

echo "Engine ready at $ENGINE"
