# speak

A Claude Code skill that turns a finished written reply into an MP3 for listening. The audio is
useful when you follow a session from your phone through Remote Control, because the speech is
generated on the machine that runs Claude Code and needs no sound card there.

## How it works

1. You ask to hear a reply, for example "read this to me" or `/speak`.
2. The main agent saves the reply to a file and starts the skill.
3. A subagent rewrites the reply for the ear. It removes code and tables, converts symbols to
   words, and rounds numbers.
4. `scripts/check_script.py` flags text that the speech engine would read wrongly.
5. `scripts/tts.py` generates the MP3 locally with Kokoro. No text goes to an outside speech service.
6. The main agent sends the MP3 to you.

The written reply stays the authority. The checker finds symbol and format problems only. It
cannot detect a changed claim, so check exact values in the written reply.

## Install

You need `uv`, `sox` with MP3 support, and `espeak-ng`.

```bash
bash speak/setup.sh
```

The script installs the engine in `~/.local/share/speak` and copies the skill to
`~/.claude/skills/speak`. The engine uses about 600 MB of disk.

## Optional: describe the listener

Create `~/.claude/speak-listener.md` to describe your language level and preferences. The subagent
reads this file, and it stays on your machine.

## Settings

The defaults in `scripts/tts.py` are voice `af_heart`, speed 0.88, and pauses of 0.45 s after a
sentence, 0.15 s after a clause, and 1 s between sections.

## Status

Tested on Rocky Linux 8 with Claude Code 2.1.319. Not tested on macOS. Sending the MP3 needs the
`SendUserFile` tool, which a subagent does not have, so the main agent sends it. If the tool is
unavailable, the skill gives you the file path.
