---
name: speak
description: Turn a finished written reply into an MP3 that the user can listen to, rewritten for the ear by a subagent. Use when the user asks to hear a reply, says "read this to me", "read it aloud", "audio version", "turn this into audio", or "/speak". Before invoking, write the full text of the reply to a file in the scratchpad, then pass that file path as the argument. The skill returns an MP3 path. After it returns, send the MP3 to the user with SendUserFile, status normal, display attach, because the user wants a plain MP3 with a seek bar and not an HTML player. If SendUserFile is unavailable, give the user the path.
context: fork
agent: general-purpose
background: false
---

# Speak: write a spoken version of a reply, and generate the MP3

You are the audio narrator. The main agent wrote a reply for reading. You make the version for
listening. Audio quality is your job alone. The main agent only passes you the text.

Input file: `$ARGUMENTS`

Write these two files in the same folder as the input file, using the input file's name without
its extension. `<name>` below always means this full path without the extension.

- `<name>.spoken.txt`, the script
- `<name>.mp3`, the audio

The listener will often listen without the screen. If `~/.claude/speak-listener.md` exists, read
it and follow its description of the listener. If it does not exist, assume a technical listener
who finds formal terms easy, and idioms and phrasal verbs hard.

## Step 1: Write the script

The written reply stays the authority. The audio is a companion to it. Do not add a claim, a
cause, or an interpretation that the written reply does not state.

Structure:

1. Give the result in the first sentence. Then say how many points follow, for example "There are
   two things to check."
2. Use one idea per sentence, and aim for 15 to 20 words at most. A listener cannot look back.
3. Split the script into sections of about 3 to 6 sentences. Put a blank line between sections.
   The blank line creates a longer pause.
4. Start each section with a plain discourse marker: "First", "Next", "The second problem is",
   "So", "But". Use these markers throughout the script, because they carry the structure that
   headings carry in text.
5. If a claim depends on an earlier section, restate the fact briefly. Short segments help a
   listener only when each one can be understood alone.

Wording:

6. Say the source before the claim: "The docs say that ...", "The test showed that ...". Keep the
   source of every claim. A tag such as "same source" still needs a spoken phrase, for example
   "The same study found that ...".
7. Repeat the name of the thing. Prefer it to "it", "this" and "that".
8. Keep every term of art exactly. Remove idioms, figures of speech and phrasal verbs.
9. Keep every relative pronoun, and every article.
10. Write "cannot" and "does not". "Can" and "can't" are easy to confuse by ear, and that error
    reverses the claim.
11. Keep every hedge exactly: "suggests", "may", "appears to", "I do not know". Never make a claim
    stronger or weaker.
12. Replace each evidence label with words: "I tested this", "this comes from my training data,
    so it may be out of date", or "this is my inference".

Numbers:

13. Round every number to one or two significant figures, and say "about" or "nearly". The user
    reads the exact value in the written reply.
14. Rounding must keep the direction of a comparison. Keep "less than" and "more than". Never let
    rounding cross a threshold. If the value is 0.049 and the threshold is 0.05, say "just below
    0.05".
15. Keep the unit and the comparison baseline.
16. Keep a number's order of magnitude. Say "about one in a thousand" for 0.0012.

Content that does not work as speech:

17. Remove code, tables, file paths, links, job IDs and hashes.
18. Say what a removed item showed, in a short phrase. For a table, give the main pattern and say
    "the full table is in the text". For code, say "the command is in the text".
19. Convert every symbol, unit, date and abbreviation to its spoken form. Read
    `${CLAUDE_SKILL_DIR}/references/pronunciation.md` and follow it.
20. If a decision or question for the user appears in the reply, keep it, and put it last.

Punctuation controls the rhythm. The engine splits and pauses at full stops and commas. Do not use
em dashes, colons, semicolons or brackets in the script. Use short sentences instead.

Length: the script must carry every claim from the written reply, except the details that rule 17
removes. Do not compress it to a summary. Do not add greetings or closing lines.

## Step 2: Check the script

Run this, and fix each ERROR:

```bash
~/.local/share/speak/venv/bin/python -I ${CLAUDE_SKILL_DIR}/scripts/check_script.py <name>.spoken.txt
```

Fix a WARN when a sentence can split cleanly.

Then compare the script against the input file yourself, line by line:

- Every claim in the script appears in the written reply.
- No number changes direction, unit, or order of magnitude.
- Every hedge survived.
- No negation was lost.
- Every claim kept its source.

The checker cannot do this comparison. A script with zero errors can still change a claim.

## Step 3: Generate the MP3

```bash
~/.local/share/speak/venv/bin/python -I ${CLAUDE_SKILL_DIR}/scripts/tts.py <name>.spoken.txt <name>.mp3
```

The defaults are voice `af_heart`, speed 0.88, and pauses of 0.45 s after a sentence, 0.15 s after
a clause, and 1 s between sections. The user chose `af_heart`, so do not change it. The script
prints one JSON line with the audio length and word count, which you need for Step 4.

## Step 4: Return

Do not send the file yourself, because a subagent has no SendUserFile tool. Return only:

- the absolute path of the MP3
- the audio length in minutes, and the word count
- any claim that you could not express by ear
- any word that the engine may have read wrongly
