---
name: paperlink_to_notion
description: Read a research paper URL and save a fully-structured literature note to the Notion Literature database. Fetches the full paper, builds an infographic, summarizes Introduction and Discussion as logical-flow narratives, saves Results as brief subsection summaries, and embeds all figures as collapsible blocks with high-res PMC images and full captions.
argument-hint: <paper-url>
---

# Paper → Notion Literature Note

Paper URL: $ARGUMENTS

Follow every step below in order. Do not skip steps.

---

## Step 1 — Resolve the paper

Run these two calls in parallel:

1. **WebSearch** `"<title or DOI from URL> full text authors abstract figures"` to confirm the paper title, authors, journal, year, and DOI.
2. **WebSearch** `"site:pmc.ncbi.nlm.nih.gov <title or DOI>"` to find the PubMed Central open-access URL (looks like `https://pmc.ncbi.nlm.nih.gov/articles/PMC<ID>/`). PMC is required for free full text and figure images.

---

## Step 2 — Fetch full article content

Run these calls in parallel using the PMC URL found in Step 1:

**Call A — Introduction + Discussion (verbatim):**
WebFetch on the PMC article URL with prompt:
> "Give me the VERBATIM text of the Introduction section and Discussion section. Do not summarize — copy the exact text. Also list all figure numbers and their complete captions verbatim."

**Call B — Results (summaries):**
WebFetch on the PMC article URL with prompt:
> "List each Results subsection heading and give a 2–3 sentence summary of what was demonstrated. Note which figures correspond to each subsection."

**Call C — Figure image URLs:**
WebFetch on the PMC article URL with prompt:
> "Find and list all figure image URLs in this page. Look for img src attributes pointing to high-resolution figure images on cdn.ncbi.nlm.nih.gov. Return each figure number and its full image URL."

PMC high-res figure URLs follow this pattern:
`https://cdn.ncbi.nlm.nih.gov/pmc/blobs/<hash>/<article_id>/<file_hash>/<filename>.jpg`

---

## Step 3 — Fetch Notion database schema

Use `mcp__plugin_Notion_notion__notion-fetch` on:
- Database URL: `https://www.notion.so/02bc4f6199d9466faf95e95f97672939`
- Data source ID: `aaf641e3-6f3f-4b21-83d4-74c6d1613794`

Check existing `journal`, `Tags`, and `manner` select options so you use exact option strings when creating the page.

---

## Step 4 — Create the Notion page

Use `mcp__plugin_Notion_notion__notion-create-pages` with:
- `parent.data_source_id`: `aaf641e3-6f3f-4b21-83d4-74c6d1613794`

### 4a — Properties to set

| Property | Value |
|---|---|
| `Name` | Full paper title \| Journal Name |
| `Author` | Comma-separated author list |
| `Published Year` | Year as number |
| `journal` | Match exactly one option from the database schema (e.g. `"Nature method"`) |
| `Tags` | JSON array string using exact option names from schema (e.g. `'["tool","single-cell","GNN🕸"]'`) |
| `Paper Signature` | Short name / acronym of the method/tool |
| `userDefined:URL` | Original paper URL |
| `status` | `"not started"` |

### 4b — Page content structure

Write the `content` field using Notion-flavored Markdown (tabs for indentation, `<details>` for toggles).

#### Section order:
1. TOC toggle
2. Infographic (see Section 5)
3. `---` divider
4. `# **Abstract**` — full abstract verbatim
5. `---` divider
6. `# **Introduction**` — logical flow summary (see format below)
7. `---` divider
8. `# **Results**` — brief summaries + collapsible figures (see format below)
9. `---` divider
10. `# **Discussion**` — logical flow summary (see format below)

#### TOC toggle (always include at the very top):
```
<details>
<summary><span color="purple">**TOC**</span> 🎨</summary>
	<table_of_contents color="gray"/>
</details>
```

---

## Step 5 — Infographic block (insert between TOC and Abstract)

Place this entire block between the `---` after the TOC toggle and `# **Abstract**`.

### 5a — Hero callout
```
::: callout {icon="🧬" color="blue_bg"}
**<Method Name>** — <Full Title>
<One sentence core concept of the paper>
**<Author1> · <Author2> · ...** | *<Journal>* Vol. <N>, pp. <X–Y> (<Year>) | DOI: <DOI>
:::
```

### 5b — Pipeline Mermaid diagram
Customize the flowchart to reflect the paper's actual workflow. Use `flowchart TB` with colored nodes. Use `<br>` for line breaks inside node labels (NOT `\n`). Enclose node labels in double quotes when they contain parentheses or special characters. Example structure:

```
```mermaid
flowchart TB
    A["Input Data<br>(description)"]
    A --> B["Step 2<br>description"]
    B --> C["Step 3<br>description"]
    C --> D["Output<br>description"]
    D --> T1 & T2 & T3 & T4
    T1["Task 1"]
    T2["Task 2"]
    T3["Task 3"]
    T4["Task 4"]
    style A fill:#2C3E50,color:#ECF0F1
    style B fill:#2980B9,color:#ECF0F1
    style C fill:#8E44AD,color:#ECF0F1
    style D fill:#27AE60,color:#ECF0F1
    style T1 fill:#E74C3C,color:#ECF0F1
    style T2 fill:#E67E22,color:#ECF0F1
    style T3 fill:#16A085,color:#ECF0F1
    style T4 fill:#2471A3,color:#ECF0F1
```
```

### 5c — Task/contribution columns (4 columns)
```
<columns>
	<column>
	::: callout {icon="<emoji>" color="purple_bg"}
	**① <Task 1 Name>**
	<2-sentence description>
	:::
	</column>
	<column>
	::: callout {icon="<emoji>" color="green_bg"}
	**② <Task 2 Name>**
	<2-sentence description>
	:::
	</column>
	<column>
	::: callout {icon="<emoji>" color="orange_bg"}
	**③ <Task 3 Name>**
	<2-sentence description>
	:::
	</column>
	<column>
	::: callout {icon="<emoji>" color="pink_bg"}
	**④ <Task 4 Name>**
	<2-sentence description>
	:::
	</column>
</columns>
```

### 5d — Applications / experiments table
```
<table header-row="true" fit-page-width="true">
	<tr>
		<td>**Application**</td>
		<td>**Key Components**</td>
		<td>**Dataset**</td>
		<td>**Key Contribution**</td>
	</tr>
	<tr>
		<td>...</td>
		<td>...</td>
		<td>...</td>
		<td>...</td>
	</tr>
</table>
```

### 5e — Stats row (4 columns)
```
<columns>
	<column>
	::: callout {icon="⚡" color="yellow_bg"}
	**<Stat label>**
	<stat value>
	:::
	</column>
	<column>
	::: callout {icon="🔌" color="gray_bg"}
	**<Stat label>**
	<stat value>
	:::
	</column>
	<column>
	::: callout {icon="📦" color="brown_bg"}
	**<Stat label>**
	<stat value>
	:::
	</column>
	<column>
	::: callout {icon="📖" color="blue_bg"}
	**<Stat label>**
	[<link text>](<url>)
	:::
	</column>
</columns>
```

---

## Step 6 — Introduction section format

Write as **bold-lead paragraphs** summarizing the logical progression of the argument. Do NOT write one long block of text. Each paragraph should start with a bold label:

```
**<Logical step label>.** <2–4 sentence summary of what this part of the intro argues or establishes.>

**<Next step label>.** <Summary>

...
```

Typical logical structure:
1. **Context / motivation** — what the field can do and why it matters
2. **Gap or limitation 1** — what current methods cannot do
3. **Gap or limitation 2** — another class of limitations
4. **The proposed solution** — what the paper does and how it works
5. **Scope / capabilities** — list of tasks/applications
6. **Implementation** — software, compatibility, availability

---

## Step 7 — Results section format

For each subsection:

```
### <Subsection heading>

<2–3 sentence brief summary: what dataset, what was done, what was shown.>

<details>
<summary>**Fig. X | <Figure title>.**</summary>
	![<Alt text>](<PMC high-res image URL>)
	**a**, <full caption panel a text>. **b**, <full caption panel b text>. ... (full verbatim caption)
</details>
```

Important:
- Use the PMC image URLs from Step 2, Call C
- Include the **full verbatim figure caption** inside the toggle (all panels a, b, c, etc.)
- Make EVERY figure a `<details>` collapsible block
- The image tag and caption text must be indented with a tab inside `<details>`

---

## Step 8 — Discussion section format

Same bold-lead paragraph format as Introduction (Step 6):

```
**<Logical step label>.** <Summary>

**<Logical step label>.** <Summary>
...
```

Typical Discussion structure:
1. **Main achievement** — what SIMBA/the tool accomplishes overall
2. **Key technical insight** — the core novelty that enables the result
3. **Benchmarking** — how it compares to existing methods
4. **Connections to prior work** — related approaches / intellectual lineage
5. **Current limitations** — honest assessment of what the method cannot yet do
6. **Future outlook** — where the field/tool goes next

---

## Quality checklist before finishing

- [ ] All 6 figures have collapsible blocks with full captions and working image URLs
- [ ] Introduction is a logical-flow summary (NOT a plain dump of the text)
- [ ] Results are brief (2–3 sentences per subsection, not full text)
- [ ] Discussion is a logical-flow summary
- [ ] Infographic has all 5 components: callout, mermaid, columns, table, stats row
- [ ] Page properties are fully filled (Name, Author, Year, Journal, Tags, Paper Signature, URL)
- [ ] Mermaid diagram uses `<br>` for line breaks (NOT `\n`)
- [ ] All figure children are indented with a tab inside `<details>`
