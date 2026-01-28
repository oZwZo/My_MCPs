# Research Planner Skill

Transforms a novel computational method and datasets into a comprehensive research plan with literature reviews, significance evaluation, hypotheses, and experimental designs.

## Quick Start

```
User: "I have a method that does X. I have datasets Y and Z. What research questions can I address?"

Assistant: [Uses this skill to guide through 8-phase research planning process]

Output: 40,000-60,000 words of research planning documentation
```

## Installation

This skill is self-contained and requires no additional dependencies. Simply ensure it's in your `.claude/skills/` directory.

**Directory Structure**:
```
.claude/
└── skills/
    └── research_planner.md  (this file)
```

**No installation needed** - Claude Code will automatically load skills from the `.claude/skills/` directory.

## Usage

### Triggering the Skill:

Describe your research situation:

```
"I have a computational method that infers time-dependent growth rates,
differentiation velocities, and diffusion parameters from single-cell RNA
data using flow matching. I've applied it to two datasets:
1) In vivo mouse bone marrow hematopoiesis time-series
2) In vitro cultured HSC differentiation time-series

What biological questions can I address with this approach?"
```

### What Happens:

The skill will guide you through 8 phases:

1. **Initial Assessment** - Ask questions about your method, data, and goals
2. **Direction Identification** - Identify 5-7 promising research directions
3. **Literature Search** - Systematic PubMed/Scholar searches for each direction
4. **Result Synthesis** - Organize findings and identify gaps
5. **Significance Evaluation** - Score and rank directions (5 criteria, 1-10 scale)
6. **Hypothesis Generation** - Formulate testable hypotheses
7. **Experimental Design** - Design computational validation experiments
8. **Research Roadmap** - Create implementation timeline and publication strategy

## Skill Workflow

### Phase 1: Initial Assessment & Questioning

**Goal**: Complete understanding of user's unique situation

**Ask About**:

**Method & Innovation**:
- What does your method do? What parameters can it infer?
- What makes it novel compared to existing methods?
- What mathematical/algorithmic framework does it use?

**Datasets Available**:
- What biological systems? (hematopoiesis, neuroscience, development, etc.)
- What data types? (scRNA-seq, multi-omics, spatial, etc.)
- In vivo or in vitro? Time-series or snapshots?
- Species? Sample size? Timepoints?

**Biological Context**:
- What biological processes are studied?
- What are the major questions in this field?
- Clinical or translational applications?

**Research Goals**:
- What do you want to achieve?
- Specific hypotheses to test?
- Ultimate goal? (publications, tools, clinical impact)

**Resources & Constraints**:
- Timeline?
- Computational resources?
- Collaborators?

**Stop Questioning When**:
- You understand the method completely
- You know all datasets and their characteristics
- You understand the biological context
- You know the user's goals and constraints

### Phase 2: Research Direction Identification

**Goal**: Identify 5-7 promising research directions

**Process**:

1. **Analyze Method Capabilities**:
   - What parameters? (growth, velocity, diffusion, etc.)
   - What comparisons? (temporal, spatial, conditions)
   - What's unique?

2. **Brainstorm Directions** (for each):
   - Core Question
   - Key Angle
   - Comparison/Contrast

3. **Output**: 5-7 directions with clear questions

**Template**:
```
Direction X: [Name]
- Core Question: [What biological question?]
- Key Angle: [How does your method provide unique insights?]
- Comparison: [In vivo vs in vitro, different lineages, etc.]
```

### Phase 3: Literature Search

**Goal**: Systematic search for each direction

**Search Strategy** (per direction):

**4 PubMed Queries**:
```
Query 1: "[System] [Process] [Aspect] single-cell"
Query 2: "[System] [Comparison] [Condition] time-series"
Query 3: "[Method-related] [System] computational modeling"
Query 4: "[Application] [System] experimental validation"
```

**1-2 Google Scholar Queries** (deep/relevance mode):
```
Query: "[System] [Key concept] comprehensive analysis"
```

**Tools Available**:
- `search_pubmed` - NCBI E-utilities API
- `search_scholar` - SerpApi Google Scholar (quick/relevance/deep modes)
- `WebSearch` - Alternative web search
- `mcp__web-search-prime__webSearchPrime` - Enhanced web search

**Batching**:
- Batch 1: Directions 1-3 (highest priority)
- Batch 2: Directions 4-6
- Batch 3: Direction 7

**For Each Paper Extract**:
- Title, authors, journal, year
- PMID/DOI
- Key findings (2-3 sentences)
- Methods used
- Relevance (HIGH/MEDIUM/LOW with justification)

### Phase 4: Result Synthesis

**Goal**: Organize and summarize literature

**For Each Direction** Create File: `{direction}/literature_search_results.md`

**Structure**:
```markdown
# [Direction Name]: Literature Search Results

## Search Strategy
- Queries, databases, date

## Key Papers Found

### Paper 1: [Title]
- **Authors**: [...]
- **Journal**: [...]
- **Year**: [...]
- **PMID/DOI**: [...]
- **Key Findings**: [...]
- **Methods**: [...]
- **Relevance**: HIGH/MEDIUM/LOW - [Why]

## Methodological Approaches
1. [Approach] - Description
2. [Approach] - Description

## Gaps and Opportunities
- What's missing
- How our method addresses gaps
- Novel contributions

## Key References
- Benchmarking papers
- Methods papers
```

**Quality Check**:
- 5-10 relevant papers per direction
- Mix of recent (2018+) and foundational
- Clear gaps identified
- Method approaches summarized

### Phase 5: Significance Evaluation

**Goal**: Score and rank directions

**5 Criteria (1-10 scale)**:

1. **Biological Impact**:
   - 10: Life-saving clinical, fundamental
   - 9: Major insights
   - 8: Important focused
   - 7: Moderate
   - 6-1: Decreasing

2. **Novelty of Approach**:
   - 10: New paradigm
   - 9: Major advance
   - 8: Significant improvement
   - 7: Moderate novelty
   - 6-1: Incremental

3. **Feasibility with Data**:
   - 10: Perfect match, ready
   - 9: Minor work needed
   - 8: Some analysis
   - 7: Moderate work
   - 6-1: Increasingly difficult

4. **Publication Potential**:
   - 10: Nature/Science/Cell certainty
   - 9: Very high
   - 8: Good
   - 7: Solid
   - 6-1: Decreasing

5. **Translational Value**:
   - 10: Clinical <2 years
   - 9: Clinical 2-5 years
   - 8: Clinical 5-10 years
   - 7: Long-term potential
   - 6-1: Decreasing

**Per Direction Scoring**:
```markdown
## Direction X: [Name]
### Overall Score: X/50

### Biological Rationale (X/10):
[Why this matters biologically]

### Current State (X/10):
[Literature summary]

### Our Contribution (X/10):
[What we add]

### Potential Impact (X/10):
[Expected outcomes]

### Translational Value (X/10):
[Clinical/practical applications]

### Recommended Priority: HIGH/MEDIUM/LOW
```

**Output File**: `significance_evaluation.md`

**Include**:
- Executive summary
- Ranked list (1-7)
- Strategic recommendations
- Which direction to focus on first

### Phase 6: Hypothesis Generation

**Goal**: Formulate testable hypotheses for top 3-5 directions

**Per Hypothesis Structure**:

```markdown
## Hypothesis X: [Title]

### Biological Question:
[What does this address?]

### Hypothesis Statement:
"If our [method] captures [aspect], then we should observe [pattern] in [data]."

### Rationale:
- Literature support
- Why testable now
- Why important

### Expected Observations:
**In System A** (e.g., in vivo):
- Parameter 1: [Expected pattern]
- Parameter 2: [Expected pattern]
- Temporal dynamics: [Expected trends]

**In System B** (e.g., in vitro):
- Divergence from System A
- Specific predictions

### Null Hypothesis:
H0: [No effect/difference]

### Alternative Hypothesis:
H1: [Specific effect with direction]

### Potential Outcomes:
1. **Strong Support** (Expected):
   - What we'd see
   - Interpretation
   - Impact

2. **Partial Support**:
   - Alternative outcome
   - Interpretation
   - Impact

3. **No Support** (Null true):
   - What it means
   - Why still valuable

### Computational Tests:
- Statistical methods
- Data requirements
- Analysis pipeline
- Success criteria
```

**Principles**:
- Specific and testable
- Quantitative predictions
- Falsifiable
- Grounded in literature
- Enabled by user's method

**Output File**: `hypotheses.md`

### Phase 7: Experimental Design

**Goal**: Design computational validation experiments

**Per Experiment Structure**:

```markdown
## Experiment X: [Name] (Testing Hypothesis X)

### Objective:
[What does this test?]

### Data Required:
**Dataset A**:
- Subsets needed
- Timepoints
- Cell types
- Sample size

**Dataset B**:
- Same specs

### Computational Steps:

#### Step 1: Data Preprocessing (Week 1)
```python
# Pseudocode/example
def preprocess(data):
    # Quality control
    # Normalization
    # Alignment
    return clean_data
```
- Duration: X time
- Deliverable: Clean data

#### Step 2: Parameter Inference (Week 2-3)
[Details...]

#### Step 3: Analysis (Week 4)
[Details...]

### Analysis Methods:

**Statistical Tests**:
- Test 1: [Name] - Purpose - Expected
- Test 2: [Name] - Purpose - Expected

**Visualizations**:
- Figure 1: [Type] - Purpose
- Figure 2: [Type] - Purpose

**Machine Learning** (if applicable):
- Algorithm
- Training/testing split
- Metrics
- Interpretation

### Expected Results:
[Quantitative predictions]

### Success Criteria:
- ✅ Criterion 1: [Measurable outcome]
- ✅ Criterion 2: [Measurable outcome]
- ✅ Criterion 3: [Measurable outcome]

### Potential Pitfalls & Solutions:
**Pitfall 1**: [What might go wrong]
- **Solution**: [How to fix it]

### Timeline:
- Week 1: [Tasks]
- Week 2: [Tasks]
- Total: X weeks

### Computational Requirements:
- Hardware: [CPU, RAM, GPU]
- Software: [Packages]
- Runtime: [Estimates]
```

**Output File**: `experimental_designs.md`

### Phase 8: Research Roadmap

**Goal**: Comprehensive implementation plan

**Structure**:

```markdown
# Research Roadmap: [Project Title]

## Executive Summary
[One-page overview]

## Priority Research Questions (Top 3)

### Question 1: [Title] ⭐ HIGHEST
- **Significance**: [Why important]
- **Approach**: [How to address]
- **Timeline**: [Months X-Y]
- **Target Journal**: [Journal]

### Question 2: [Title]
[Same structure]

### Question 3: [Title]
[Same structure]

## Implementation Plan

### Phase 1: [Name] (Months 1-3)
**Focus**: [Primary direction]
- Tasks:
  - [Task 1] - Owner - Due
  - [Task 2] - Owner - Due
- Deliverables:
  - [Deliverable 1]
  - [Deliverable 2]
- Milestones:
  - [Milestone 1] - Criteria

### Phase 2: [Name] (Months 3-6)
[Same structure]

## Publication Strategy

### Paper 1: [Title]
- **Focus**: [Primary contribution]
- **Target Journals** (order):
  1. [Journal 1] - Why good fit
  2. [Journal 2] - Backup
  3. [Journal 3] - Second backup
- **Timeline**: Submit Month X
- **Key Selling Points**:
  - Point 1: [Novel contribution]
  - Point 2: [Impact]

### Paper 2 & 3: [Same structure]

## Computational Resources
- Hardware: [Specs, cost]
- Software: [Packages]
- Data: [Available, optional]

## Funding Opportunities
- Immediate: [Fellowships, pilots]
- Long-term: [Grants, industry]

## Risk Management
- Technical Risk 1: [Mitigation]
- Publication Risk 2: [Mitigation]

## Success Metrics
- Academic: [Publications, citations]
- Clinical: [Applications, impact]
- Foundation: [Grants, collaborations]

## Next Steps (Week 1-2)
1. [Immediate action 1]
2. [Immediate action 2]

## Timeline Summary
| Phase | Duration | Focus | Deliverables |
|-------|----------|-------|--------------|
| Phase 1 | Months X-Y | [Focus] | [Deliverables] |

**Total to First Publication**: X months
**Total to All Publications**: Y months
```

**Output File**: `research_roadmap.md`

## Output File Structure

All research planning documents organized as:

```
project_research/
├── 01_direction_one/
│   └── literature_search_results.md
├── 02_direction_two/
│   └── literature_search_results.md
├── 03_direction_three/
│   └── literature_search_results.md
├── ...
├── significance_evaluation.md
├── hypotheses.md
├── experimental_designs.md
├── research_roadmap.md
└── README.md
```

## Adaptation Guidelines

### For Different Biological Systems:

**Hematopoiesis**:
- Focus: Lineage commitment, stem cell dynamics, in vivo vs in vitro
- Key: Fate decisions, differentiation rates, niche interactions

**Neuroscience**:
- Focus: Cell type specification, connectivity, development vs disease
- Key: Neural differentiation, circuits, regional identity

**Developmental Biology**:
- Focus: Embryogenesis, organogenesis, temporal patterning
- Key: Morphogenesis, fate maps, signaling

**Cancer**:
- Focus: Tumor heterogeneity, treatment response, metastasis
- Key: Clonal evolution, drug resistance, microenvironment

**Immunology**:
- Focus: Immune activation, differentiation, pathogen response
- Key: T/B cell activation, maturation, inflammation

### For Different Data Types:

**scRNA-seq**: Leverage gene expression, trajectories, RNA velocity
**Multi-omics**: Integrate ATAC, proteomics, spatial
**Spatial**: Use location, cell-cell interactions, neighborhoods
**Time-series**: Dynamic modeling, rates, change points

## Key Principles

1. **Question First**: Don't assume, ask until complete understanding
2. **Literature-Driven**: Every hypothesis grounded in papers
3. **Feasibility**: Must be testable with available data
4. **Impact**: Prioritize high-impact directions
5. **Rigor**: Statistical validation, reproducibility
6. **Publication**: Design experiments with papers in mind

## Quality Assurance

**Before Finalizing**:

✅ **Literature**: 5-10 papers/direction, recent + foundational, gaps clear
✅ **Evaluation**: Consistent scoring, detailed justification
✅ **Hypotheses**: Specific, testable, quantitative, grounded
✅ **Experiments**: Detailed steps, statistical tests, success criteria
✅ **Roadmap**: Realistic timeline, clear milestones

## Example Output

**Input**:
```
Method: Time-dependent flow matching for single-cell data
Datasets: Mouse bone marrow hematopoiesis (in vivo + in vitro)
```

**Output** (after 8 phases):
- 3 literature reviews (50+ papers)
- Significance evaluation (7 directions ranked)
- 4 testable hypotheses
- 4 detailed experimental designs (8-week pipelines)
- Research roadmap (15-month timeline, 3 papers planned)
- **Total**: ~45,000 words of documentation

## Tips for Success

1. **Start Simple**: 1-2 directions first, expand if needed
2. **Be Specific**: Vague → Clear questions → Better hypotheses
3. **Stay Focused**: Don't answer everything, prioritize
4. **Think Publication**: Every experiment → paper contribution
5. **Validate Often**: Check assumptions with user
6. **Document**: Create clear, reusable docs

## Success Metrics

When executed successfully, this skill produces:

- ✅ **50-70 relevant papers** identified and summarized
- ✅ **5-7 research directions** with clear questions
- ✅ **3-5 testable hypotheses** with detailed validation
- ✅ **Ranked priorities** with quantitative justification
- ✅ **Publication strategy** for 2-3 papers
- ✅ **15-month roadmap** with phases and milestones
- ✅ **40,000-60,000 words** of planning documentation

## Notes

- **Duration**: 3-4 hours to complete all 8 phases thoroughly
- **Adaptable**: Works for any biological system or computational method
- **Emphasis**: High-impact, publishable research
- **Output**: Publication-ready research plans
