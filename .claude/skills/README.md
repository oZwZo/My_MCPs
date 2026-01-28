# Claude Code Skills

This directory contains custom skills for Claude Code.

## Available Skills

### 1. research_planner.md
**Comprehensive research planning workflow**

Transforms a novel computational method and datasets into a complete research plan with:
- Literature reviews (PubMed + Google Scholar)
- Significance evaluation and prioritization
- Testable hypothesis generation
- Computational experimental design
- Publication strategy and roadmap

**When to use**:
- You have a novel computational or experimental method
- You have biological datasets (single-cell, multi-omics, etc.)
- You need to identify high-impact research questions
- You want a complete research plan with hypotheses and experiments

**Example usage**:
```
"I have a method that infers time-dependent growth rates from single-cell data.
I've applied it to mouse hematopoiesis datasets (in vivo and in vitro).
What biological questions can I address?"
```

**Output**: 40,000-60,000 words of research planning documentation

**Features**:
- 8-phase systematic workflow
- Literature-driven hypothesis generation
- Quantitative significance evaluation (5 criteria)
- Detailed computational experimental designs
- Publication strategy (target journals, timelines)
- Implementation roadmap (15-month plans)

**Duration**: 3-4 hours to complete all phases

---

### 2. questioning_pipeline.md
**Detailed research planning pipeline with examples**

Complete workflow documentation with hematopoiesis research as a detailed example.

**When to use**:
- You want to understand the research planning methodology
- You need examples for different biological systems
- You're adapting the workflow to new domains

**Contents**:
- Detailed 8-phase workflow
- Templates for each phase
- Real examples from hematopoiesis research
- Adaptation guidelines for different systems
- Quality assurance checklists

---

## How Skills Work in Claude Code

Skills are automatically loaded from `.claude/skills/` directory when Claude Code starts.

**No installation needed** - just place `.md` skill files in this directory and they'll be available.

**Skill format**:
- Markdown files with structured sections
- Trigger keywords in the content
- Clear workflow descriptions
- Output specifications

**Creating custom skills**:
1. Create `.md` file in this directory
2. Add skill overview, workflow, examples
3. Restart Claude Code
4. Skill is automatically available

---

## Installation on New Machines

To use these skills on another machine:

1. **Clone the repository**:
   ```bash
   git clone git@github.com:oZwZo/My_MCPs.git
   cd My_MCPs
   ```

2. **Skills are automatically available**:
   - Located in `.claude/skills/`
   - Claude Code loads them automatically
   - No additional setup needed

3. **Verify skills are loaded**:
   - Check Claude Code settings
   - Skills should appear in available skills list

---

## Skill Development

**Based on**:
- Real research workflows
- Best practices in computational biology
- Literature review methodologies
- Hypothesis-driven research

**Tested on**:
- Hematopoietic stem cell research
- Single-cell RNA-seq analysis
- Time-dependent computational modeling
- In vivo vs in vitro comparisons

**Adaptable to**:
- Any biological system (neuroscience, cancer, immunology, development)
- Any data type (scRNA-seq, multi-omics, spatial, time-series)
- Any computational method (machine learning, statistical modeling, simulation)

---

## Support

For questions or issues:
- Check the skill documentation for detailed instructions
- Review example outputs in skill files
- Adapt templates to your specific research context

---

## Version History

- **v1.0** (2025-01-27): Initial research_planner and questioning_pipeline skills
  - Developed from hematopoiesis research project
  - 50+ papers reviewed
  - 45,000+ words of documentation generated
  - Successfully validated on real research project
