# Examples

`example_paper_info.json` is a small synthetic input that exercises every
top-level field of the `paper_info` schema. It does **not** describe any real
paper — its only purpose is to smoke-test the renderer.

Try it:

```bash
python3 ../scripts/render_html.py \
    --json example_paper_info.json \
    --out  /tmp/demo_guide.html
open /tmp/demo_guide.html
```

When authoring a learning guide for a real paper, build your own
`paper_info` JSON by copying this file and replacing each field with
paraphrased content drawn from the paper and its public abstract / press
materials. **Do not paste long verbatim passages from closed-access journal
text** — keep paraphrases, cite the source, and link out to the canonical
figures.
