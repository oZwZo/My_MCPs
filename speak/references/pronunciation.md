# Pronunciation list

The engine reads text through espeak-ng. Each entry below was tested on the Kokoro
phonemizer unless marked untested. Add new entries when the user reports a wrong word.

| Written form | Write this in the script | Reason |
|---|---|---|
| `p < 0.05` | p is less than 0.05 | the engine drops "<" |
| `R²` | R squared | the engine says "R two" |
| `1.5e-3` | about one in a thousand, or about 0.002 | the engine drops the minus |
| `A -> B` | from A to B | the engine drops the arrow and reads "A" as the article |
| `ICC` | I C C | the engine says "ike" |
| `CSD3` | C S D 3, or the cluster | safe either way |
| `scRNA-seq` | single-cell RNA sequencing | clearer to the ear |
| `ATAC-seq` | ATAC sequencing | untested as a phrase; the raw form is read as "atac seck" |
| `10x Genomics` | ten X Genomics | the engine says "ten ex", which is acceptable |
| `k=5` | k equals five | safe |
| `Wasserstein-2` | Wasserstein 2 | safe |
| `tts.py`, TTS | the speech script, or text to speech | a file name is not speech, and lowercase tts may be read as a word (untested) |
| `vs.` | against, or compared with | the engine says "V S" |
| `e.g.` | for example | the engine says "E G" |
| `i.e.` | in other words | the engine says "I E" |
| dates | November the seventh | the engine reads the dashes aloud |
| file paths | the name of the thing, such as the speak folder | the engine reads every slash |
| job numbers, commit hashes | the Slurm job | the engine reads a job ID as forty million |
