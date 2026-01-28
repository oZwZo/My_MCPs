# Research Planning Pipeline Skill

## Overview

This skill guides researchers through a systematic literature review and research planning process. It transforms a novel computational method and datasets into a comprehensive research plan with:
- Literature reviews across multiple research directions
- Significance evaluation and prioritization
- Testable hypothesis generation
- Computational experimental design
- Publication strategy

## Use Cases

Use this skill when you have:
- A **novel computational method** or analysis approach
- **Single-cell or multi-omics datasets** (in vivo, in vitro, time-series, etc.)
- Need to identify **high-impact biological questions** your method can address
- Want to generate a **complete research roadmap** with hypotheses and experimental designs

## Workflow

### Phase 1: Initial Assessment & Questioning

**Goal**: Understand user's background, method, and data through iterative questioning.

#### Key Questions to Ask:

1. **Method & Innovation**:
   - What is your computational method? What does it do?
   - What parameters can it infer? (e.g., growth rates, velocities, diffusion coefficients)
   - What makes it novel compared to existing methods?
   - What mathematical framework does it use? (e.g., flow matching, optimal transport, neural networks)

2. **Datasets Available**:
   - What biological systems are studied? (e.g., hematopoiesis, neuroscience, development)
   - What type of data? (scRNA-seq, multi-omics, spatial, etc.)
   - In vivo or in vitro? Time-series or snapshots?
   - What species? (mouse, human, other)
   - Sample size and timepoints?

3. **Biological Context**:
   - What biological process are you studying?
   - What are the key biological questions in this field?
   - What are the major clinical or translational applications?
   - Who is the target audience for this research? (biologists, clinicians, computational biologists)

4. **Research Goals**:
   - What do you want to achieve with this analysis?
   - Are there specific hypotheses you want to test?
   - What is your ultimate goal? (publications, clinical applications, tool development)

5. **Constraints & Resources**:
   - What is your timeline?
   - What computational resources are available?
   - Do you have collaborators? What are their expertise areas?

**Outcome**: Comprehensive understanding of user's unique situation and needs.

---

### Phase 2: Research Direction Identification

**Goal**: Identify 5-7 promising research directions based on the method and data.

#### Process:

1. **Analyze Method Capabilities**:
   - What parameters can the method infer?
   - What comparisons can it make? (temporal, spatial, condition-specific)
   - What is unique about this approach?

2. **Brainstorm Research Directions**:
   For each direction, define:
   - **Core Question**: What biological question does this address?
   - **Key Angle**: How does your method provide unique insights?
   - **Comparison**: In vivo vs in vitro, different conditions, lineages, etc.

3. **Preliminary Prioritization**:
   - Rate directions based on:
     - Biological importance
     - Novelty of insights
     - Feasibility with available data
     - Publication potential

**Output**: 5-7 well-defined research directions with clear questions.

---

### Phase 3: Literature Search Strategy

**Goal**: Systematically search PubMed and Google Scholar for each direction.

#### Search Design:

For each research direction, design 3-4 specific queries:

**Query Template**:
```
"[Biological system] [Process/phenomenon] [Aspect of interest] [Methodology/Modality]"
```

**Examples**:
- "hematopoietic stem cell fate decision temporal dynamics single-cell"
- "in vivo bone marrow versus in vitro culture hematopoiesis single-cell"
- "lineage-specific differentiation rate hematopoiesis time-series"

#### Search Tools:

1. **PubMed/NCBI**:
   - Use `search_pubmed` tool
   - 10-20 results per search
   - Focus on recent papers (last 5-7 years)
   - Extract: PMID, title, authors, journal, year

2. **Google Scholar**:
   - Use `search_scholar` tool with 3 modes:
     - `quick`: First 10 papers (exploratory)
     - `relevance`: Top from 200 (comprehensive)
     - `deep`: Citation-based expansion (foundational)
   - Extract: title, summary, link, authors, year, journal, citation count

#### Batching Strategy:

- **Batch 1** (Highest Priority): Directions 1-3
- **Batch 2** (Medium Priority): Directions 4-6
- **Batch 3** (Specific): Direction 7

**Per-Direction Search Structure**:
```
1. PubMed Query 1 (primary aspect)
2. PubMed Query 2 (secondary aspect)
3. PubMed Query 3 (methodological)
4. PubMed Query 4 (comparative/applied)
5. Google Scholar Query (deep/relevance mode for comprehensive coverage)
```

**Output**: 5-10 relevant papers per direction with key details.

---

### Phase 4: Result Synthesis

**Goal**: Organize and summarize literature search results.

#### For Each Research Direction:

Create a markdown file: `{direction}/literature_search_results.md`

**Structure**:
```markdown
# [Direction Name]: Literature Search Results

## Search Strategy
- Queries used
- Databases searched
- Date of search

## Key Papers Found

### Paper 1: [Title]
- **Authors**: [...]
- **Journal**: [...]
- **Year**: [...]
- **PMID/DOI**: [...]
- **Citations**: [...]
- **Key Findings**: [...]
- **Methods**: [...]
- **Relevance to Our Work**: [...] (HIGH/MEDIUM/LOW with reason)

## Methodological Approaches Identified
1. [Approach 1] - Description
2. [Approach 2] - Description

## Gaps and Opportunities
- What's missing in current literature
- How our method addresses these gaps
- Novel contributions we can make

## Key References for Methods
- Benchmarking papers
- Computational approaches
- Experimental designs
```

**Key Activities**:
1. Extract paper metadata (title, authors, journal, year, PMID/DOI)
2. Summarize key findings (2-3 sentences per paper)
3. Identify methodological approaches used
4. Note relevance to user's work (HIGH/MEDIUM/LOW)
5. Identify gaps in current literature
6. Highlight how user's method fills these gaps

**Output**: Organized literature reviews for each direction.

---

### Phase 5: Significance Evaluation

**Goal**: Score and rank research directions based on multiple criteria.

#### Evaluation Criteria (1-10 scale):

1. **Biological Impact**:
   - 10: Life-saving clinical applications, fundamental understanding
   - 9: Major biological insights
   - 8: Important focused questions
   - 7: Moderate impact
   - 6-1: Decreasing impact

2. **Novelty of Approach**:
   - 10: Completely new paradigm, no existing methods
   - 9: Major advance over existing
   - 8: Significant improvement
   - 7: Moderate novelty
   - 6-1: Incremental changes

3. **Feasibility with Available Data**:
   - 10: Perfect match, no additional work needed
   - 9: Minor annotations/computations required
   - 8: Some additional analysis needed
   - 7: Moderate additional work
   - 6-1: Increasingly difficult

4. **Publication Potential**:
   - 10: Nature/Science/Cell level certainty
   - 9: Very high probability
   - 8: Good probability
   - 7: Solid probability
   - 6-1: Decreasing likelihood

5. **Translational Value**:
   - 10: Direct clinical application <2 years
   - 9: Clear clinical path 2-5 years
   - 8: Clinical path 5-10 years
   - 7: Long-term clinical potential
   - 6-1: Decreasing translational likelihood

#### Scoring Process:

For each direction:
1. Score each criterion (1-10)
2. Sum scores (maximum 50)
3. Provide detailed justification for each score
4. Identify recommended priority (HIGH/MEDIUM/LOW)

#### Output Document:

Create: `significance_evaluation.md`

**Structure**:
```markdown
# Research Direction Significance Evaluation

## Executive Summary
- Top 3 ranked directions
- Recommended primary focus
- Strategic recommendations

## Evaluation Criteria
[Explanation of each criterion]

## Direction 1: [Name]
### Overall Score: X/50
### Biological Rationale: [Why this matters]
### Current State of Field: [Literature summary]
### Our Unique Contribution: [What we add]
### Potential Impact: [Expected outcomes]
### Recommended Priority: [HIGH/MEDIUM/LOW]

## Ranked List of Directions
1. Direction X (Score: Y/50) - Priority
2. Direction Y (Score: Z/50) - Priority
...

## Strategic Recommendations
- Which direction to focus on first
- Publication strategy
- Timeline recommendations
```

**Output**: Ranked list with detailed justifications.

---

### Phase 6: Hypothesis Generation

**Goal**: Formulate specific, testable hypotheses for top 3-5 directions.

#### Hypothesis Template:

For each hypothesis, provide:

```markdown
## Hypothesis X: [Title] ⭐ Priority

### Biological Question:
[What biological question does this address?]

### Hypothesis Statement:
"If our [method] captures [specific aspect], then we should observe [specific pattern] in the [system/data]."

### Rationale:
- Why this hypothesis is important
- Literature supporting it
- How your method enables testing it

### Expected Observations:
- **In System A** (e.g., in vivo): [Specific patterns]
- **In System B** (e.g., in vitro): [Specific patterns]
- **Quantitative predictions**: [Expected values/trends]

### Null Hypothesis:
H0: [No effect, no difference, or random pattern]

### Alternative Hypothesis:
H1: [Specific effect/difference with direction]

### Potential Outcomes:
1. **Strong Support**: [What we expect to see]
   - Interpretation: [What it means]
   - Impact: [Why it matters]

2. **Partial Support**: [Alternative outcome]
   - Interpretation: [Revised understanding]
   - Impact: [Still valuable]

3. **No Support** (Null true): [If hypothesis wrong]
   - Interpretation: [What it tells us]
   - Impact: [Still advances knowledge]

### Computational Tests:
- Statistical methods
- Data requirements
- Analysis pipeline
- Success criteria
```

**Key Principles**:
- **Specific**: Clear, testable predictions
- **Quantitative**: Numerical expectations where possible
- **Falsifiable**: Can be proven wrong
- **Grounded**: Based on literature and method capabilities
- **Novel**: Addresses gaps not answered by existing work

**Output Document**:

Create: `hypotheses.md`

**Structure**:
```markdown
# Testable Hypotheses

## Overview
- Number of hypotheses
- How they relate to each other
- Priority ranking

## Hypothesis 1: [Title]
[Full hypothesis specification as above]

## Hypothesis 2: [Title]
[Full hypothesis specification as above]

...

## Cross-Hypothesis Analysis
- How hypotheses relate
- Dependencies between them
- Testing order recommendations
```

**Output**: 3-5 detailed, testable hypotheses.

---

### Phase 7: Experimental Design

**Goal**: Design computational experiments to test each hypothesis.

#### Experiment Template:

For each experiment:

```markdown
## Experiment X: [Name] (Testing Hypothesis X)

### Objective:
[What does this experiment test?]

### Data Required:
- **Dataset A** (e.g., in vivo):
  - Subsets needed
  - Timepoints required
  - Cell types needed
  - Sample size considerations

- **Dataset B** (e.g., in vitro):
  - Same specifications

### Computational Steps:

#### Step 1: Data Preprocessing
- Quality control
- Normalization
- Alignment (if comparing systems)
- Expected duration: X time

#### Step 2: Parameter Inference
- Apply computational method
- Extract time-dependent parameters
- Output: Parameter arrays

#### Step 3: Analysis
- Statistical tests
- Comparative analysis
- Pattern detection

[Continue with all steps...]

### Analysis Methods:

#### Statistical Tests:
- Test 1: [Name] - Purpose - Expected outcome
- Test 2: [Name] - Purpose - Expected outcome

#### Visualization:
- Figure 1: [Description] - Purpose
- Figure 2: [Description] - Purpose

#### Machine Learning (if applicable):
- Algorithm: [Name]
- Training/testing split
- Performance metrics
- Interpretation methods

### Expected Results:
- What we expect to see
- Quantitative predictions
- How results support/refute hypothesis

### Success Criteria:
- ✅ Criterion 1: [Specific measurable outcome]
- ✅ Criterion 2: [Specific measurable outcome]
- ✅ Criterion 3: [Specific measurable outcome]

### Potential Pitfalls and Solutions:
- **Pitfall 1**: [What might go wrong]
  - **Solution**: [How to address it]
- **Pitfall 2**: [What might go wrong]
  - **Solution**: [How to address it]

### Timeline:
- Week 1: [Tasks]
- Week 2: [Tasks]
- Total: X weeks

### Computational Requirements:
- Hardware: [CPU, RAM, GPU]
- Software: [Packages, languages]
- Runtime estimates
```

**Key Considerations**:
- **Feasibility**: Can this be done with available data/resources?
- **Rigor**: Statistical validation, reproducibility
- **Efficiency**: Parallel processing, optimization
- **Validation**: Cross-validation, benchmarking, comparison to ground truth

**Output Document**:

Create: `experimental_designs.md`

**Structure**:
```markdown
# Computational Experiments to Test Hypotheses

## Overview
- Number of experiments
- Total estimated time
- Resource requirements

## Experiment 1: [Name]
[Full experimental design as above]

## Experiment 2: [Name]
[Full experimental design as above]

...

## Integration Plan
- How experiments relate
- Which to run first
- Dependencies between experiments

## Quality Assurance
- Validation strategies
- Reproducibility measures
- Statistical power analysis
```

**Output**: Detailed computational pipelines for each hypothesis.

---

### Phase 8: Final Research Roadmap

**Goal**: Synthesize everything into a comprehensive implementation plan.

#### Roadmap Components:

```markdown
# Research Roadmap: [Project Title]

## Executive Summary
[One-page overview of entire project]

## Priority Research Questions (Top 3)

### Question 1: [Title]
- **Significance**: [Why it matters]
- **Approach**: [How to address it]
- **Timeline**: [Months needed]
- **Target Journal**: [Where to publish]

### Question 2: [Title]
[Same structure]

### Question 3: [Title]
[Same structure]

## Implementation Plan

### Phase 1: [Name] (Months X-Y)
- **Tasks**:
  - Task 1: [Description] - Owner - Due date
  - Task 2: [Description] - Owner - Due date
- **Deliverables**:
  - Deliverable 1: [Description]
  - Deliverable 2: [Description]
- **Milestones**:
  - Milestone 1: [Description] - Criteria

### Phase 2: [Name] (Months Y-Z)
[Same structure]

[Continue for all phases...]

## Publication Strategy

### Paper 1: [Title]
- **Focus**: [Primary contribution]
- **Target Journals** (in order):
  1. [Journal 1] - Why it's a good fit
  2. [Journal 2] - Backup option
  3. [Journal 3] - Second backup
- **Submission Timeline**: Month X
- **Expected Decision**: X-Y months
- **Key Selling Points**:
  - Point 1: [Novel contribution]
  - Point 2: [Impact]
  - Point 3: [Broader relevance]

### Paper 2: [Title]
[Same structure]

### Paper 3: [Title]
[Same structure]

## Computational Resources Needed

### Hardware:
- **CPU**: [Cores, speed]
- **RAM**: [GB]
- **Storage**: [TB]
- **GPU**: [If needed]
- **Estimated Cost**: $X

### Software:
- **Core Stack**: [Languages, packages]
- **Development Tools**: [IDEs, version control]
- **Visualization**: [Libraries]

### Datasets:
- **Currently Available**: ✅ [List]
- **Optional Addition**: [If needed]

## Funding Opportunities

### Immediate (Months 1-6):
- Fellowship X - [Focus area]
- Grant Y - [Why good fit]

### Long-term (Months 6-12):
- Grant Z - [Larger award]
- Industry collaboration - [Potential partners]

## Risk Management

### Technical Risks:
- **Risk 1**: [Description]
  - **Probability**: [High/Medium/Low]
  - **Impact**: [High/Medium/Low]
  - **Mitigation**: [How to address]

### Publication Risks:
- **Risk 2**: [Description]
  - **Probability**: [High/Medium/Low]
  - **Impact**: [High/Medium/Low]
  - **Mitigation**: [How to address]

## Success Metrics

### Academic Success:
- ✅ [X] high-impact publications
- ✅ [Y] citations within Z years
- ✅ [Software adoption] metrics

### Clinical/Translational Success:
- ✅ [Specific outcomes]
- ✅ [Adoption metrics]

### Research Foundation:
- ✅ [Grant funding]
- ✅ [Collaborations]
- ✅ [Recognition]

## Next Steps (Immediate - Week 1-2)

1. **Set up computational environment**
   - Install dependencies
   - Configure tools
   - Initialize project structure

2. **Load and inspect data**
   - Verify data integrity
   - Understand structure
   - Initial QC

3. **Implement core pipeline**
   - Parameter inference
   - Initial analysis
   - Validation checks

## Timeline Summary

| Phase | Duration | Focus | Deliverables |
|-------|----------|-------|--------------|
| Phase 1 | Months X-Y | [Focus] | [Deliverables] |
| Phase 2 | Months Y-Z | [Focus] | [Deliverables] |

**Total Timeline to First Publication**: X months
**Total Timeline to All Publications**: Y months
```

**Output Document**:

Create: `research_roadmap.md`

**Output**: Comprehensive implementation plan with timelines, milestones, and success metrics.

---

## File Structure

Organize all outputs in a structured directory:

```
project_research/
├── 01_direction_one_name/
│   └── literature_search_results.md
├── 02_direction_two_name/
│   └── literature_search_results.md
├── 03_direction_three_name/
│   └── literature_search_results.md
├── ...
├── significance_evaluation.md
├── hypotheses.md
├── experimental_designs.md
├── research_roadmap.md
└── README.md  # Quick start guide
```

---

## Key Principles

### 1. Iterative Questioning First
- Don't assume anything about user's background
- Ask detailed questions about:
  - Method capabilities and innovation
  - Data characteristics and limitations
  - Biological context and goals
  - Resources and constraints
- Only proceed when you have complete understanding

### 2. Literature-Driven
- Every hypothesis grounded in existing literature
- Identify genuine gaps, don't just rephrase known questions
- Leverage user's unique method to address unmet needs

### 3. Feasibility-Focused
- All hypotheses must be testable with available data
- Experimental designs must be computationally feasible
- Timeline must be realistic

### 4. Impact-Oriented
- Prioritize research directions with highest impact
- Consider both academic and translational impact
- Publication strategy from the start

### 5. Rigorous Standards
- Statistical validation in every experiment
- Clear success criteria
- Reproducibility measures
- Quality assurance checkpoints

---

## Adaptation Guidelines

### For Different Biological Systems:

**Hematopoiesis** (as in this example):
- Focus on: Lineage commitment, stem cell dynamics, in vivo vs in vitro
- Key questions: Fate decisions, differentiation rates, niche interactions

**Neuroscience**:
- Focus on: Cell type specification, connectivity, development vs disease
- Key questions: Neural differentiation, circuit formation, regional identity

**Developmental Biology**:
- Focus on: Embryogenesis, organogenesis, temporal patterning
- Key questions: Morphogenesis, cell fate maps, signaling dynamics

**Cancer**:
- Focus on: Tumor heterogeneity, treatment response, metastasis
- Key questions: Clonal evolution, drug resistance, microenvironment

**Immunology**:
- Focus on: Immune cell activation, differentiation, response to pathogens
- Key questions: T cell activation, B cell maturation, inflammatory responses

### For Different Data Types:

**Single-Cell RNA-seq**:
- Leverage: Gene expression, cell type identification, trajectory inference
- Methods: RNA velocity, pseudotime, clustering

**Multi-omics**:
- Leverage: ATAC-seq, proteomics, spatial transcriptomics
- Methods: Multi-modal integration, cross-modality validation

**Spatial Data**:
- Leverage: Location information, cell-cell interactions
- Methods: Spatial autocorrelation, neighborhood analysis

**Time-Series**:
- Leverage: Temporal dynamics, differentiation trajectories
- Methods: Dynamic modeling, rate inference, change point detection

---

## Quality Assurance Checklist

Before finalizing the research plan, verify:

✅ **Literature Review**:
- [ ] At least 5-10 relevant papers per direction
- [ ] Papers from recent years (2018-2025)
- [ ] Mix of foundational and cutting-edge work
- [ ] Clear gaps identified

✅ **Significance Evaluation**:
- [ ] All directions scored consistently
- [ ] Justifications are detailed and evidence-based
- [ ] Ranking is logical and defensible
- [ ] Priority recommendations are clear

✅ **Hypotheses**:
- [ ] All hypotheses are specific and testable
- [ ] Null and alternative hypotheses clearly defined
- [ ] Expected outcomes are quantitative where possible
- [ ] Grounded in literature and method capabilities

✅ **Experimental Designs**:
- [ ] Steps are detailed and actionable
- [ ] Statistical tests are appropriate
- [ ] Success criteria are measurable
- [ ] Pitfalls identified with solutions

✅ **Roadmap**:
- [ ] Timeline is realistic
- [ ] Milestones are specific
- [ ] Resources match requirements
- [ ] Risk mitigation strategies in place

---

## Tips for Success

1. **Start Simple**: Begin with 1-2 research directions, expand if needed
2. **Be Specific**: Vague questions lead to vague answers
3. **Stay Focused**: Don't try to answer everything at once
4. **Think Publicationally**: Every experiment should contribute to a paper
5. **Validate Often**: Check assumptions with user throughout process
6. **Document Everything**: Create clear, reusable documentation

---

## Example Usage

**User Input**:
```
I have a method that infers time-dependent growth and differentiation rates from single-cell data.
Applied to mouse hematopoiesis in vivo and HSC differentiation in vitro.
What biological questions can I address?
```

**Skill Execution**:

1. **Phase 1**: Ask detailed questions about:
   - Method details (flow matching? parameters?)
   - Data specifics (timepoints? sample size?)
   - Goals (publications? clinical applications?)

2. **Phase 2**: Identify 7 research directions:
   - Time-dependent fate decisions
   - In vivo vs in vitro comparison
   - Lineage-specific patterns
   - Critical transitions
   - Niche regulation
   - Stem cell heterogeneity
   - Differentiation efficiency

3. **Phase 3-4**: Literature search and synthesis
   - Search PubMed/Scholar for each direction
   - Summarize 50+ papers
   - Identify gaps

4. **Phase 5**: Significance evaluation
   - Score each direction (Biological Impact, Novelty, Feasibility, Publication, Translation)
   - Rank: In vivo vs in vitro (46/50) - HIGHEST PRIORITY

5. **Phase 6**: Generate hypotheses
   - Culture-induced temporal divergence
   - Lineage-specific fingerprints
   - Acceleration phases
   - Niche communication diffusion

6. **Phase 7**: Design experiments
   - 8-week computational pipelines
   - Statistical methods
   - Success criteria

7. **Phase 8**: Create roadmap
   - 15-month timeline to 3 papers
   - Publication strategy
   - Funding opportunities

**Output**: Complete research plan with 50+ pages of documentation!

---

## Notes

- This skill typically generates 40,000-60,000 words of documentation
- Process takes 3-4 hours to complete thoroughly
- Adaptable to any biological system or computational method
- Emphasis on high-impact, publishable research
