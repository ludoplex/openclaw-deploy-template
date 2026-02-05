# Patterns Reference

Detailed seeking, processing, analysis, and verification pattern expansions.

## Seeking Patterns

### Insider Terminology Probe
What do practitioners call this? Search for their words, not yours.

Steps:
1. Identify the domain
2. Find 2-3 practitioners (forums, papers, job postings)
3. Extract their vocabulary
4. Use their terms in queries

### Structural Exploitation
Where would this document be in their filesystem? What would it be titled internally? What format?

Questions:
- What naming convention would they use?
- What file format is standard in this domain?
- Where do organizations typically store this type of information?
- What adjacent documents would link to this?

### Layer Awareness

| Layer | Character | Access Method |
|-------|-----------|---------------|
| Public | SEO-polluted, noisy, adversarially optimized against you | Standard search, but filter aggressively |
| Internal | Requires knowing it exists, not advertised | Domain-specific searches, professional forums |
| Obscured | Exists but buried, requires specific knowledge | Insider terminology, structural exploitation |
| Protected | Access-controlled | Social engineering, credentials, FOIA |
| Denied | Existence concealed | Inference from observables, leaks, discovery |

### Triangulation Requirement
One source is hypothesis. Two concordant sources with different failure modes is evidence. Three is stronger. One source repeated many times is still one source.

Different failure modes means:
- Different authors
- Different methodological approaches
- Different incentive structures
- Different access to ground truth
- Different potential biases

### Modality Selection

| Information Type | Primary Modality |
|------------------|------------------|
| Current state of physical thing | Direct observation, sensors, images |
| Historical record | Archives, filings, databases |
| What someone knows | Human sources, interviews |
| What organization does | Filings, leaks, observation, inference |
| Technical specification | Primary documentation, standards bodies |
| Economic data | Regulatory filings, market data APIs |
| Scientific claim | Primary literature, experimental data |
| Legal status | Court records, regulatory filings |
| Hidden information | Inference from observables, FOIA, discovery |

Do not default to web search. Select appropriate modality.

---

## Processing Patterns

### Decomposition Cascade
Take it apart. Take the parts apart. Stop when you hit bedrock or acknowledged gap. Mark the gaps.

Format:
```
SYSTEM
├── Component A
│   ├── Sub-component A1 [UNDERSTOOD]
│   └── Sub-component A2 [UNDERSTOOD]
├── Component B [PARTIALLY UNDERSTOOD]
│   └── [GAP: mechanism unclear]
└── Component C
    └── [OPAQUE: cannot decompose further]
```

### Mechanism Demand
"How does this actually happen?" No metaphors. No analogies. The actual physical/logical/causal chain.

Questions:
- What is the sequence of steps?
- What causes each step to lead to the next?
- What physical/logical laws govern each transition?
- Where does the explanation use a word that could be unpacked but isn't?

No mechanism = not understood.

### Failure Mode Search
How can each component fail? What happens then?

For each component:
1. List failure modes
2. Identify dependencies
3. Map cascade effects
4. Note assumptions that must hold

### Assumption Surfacing
What must be true for this to hold?

Categories:
- Existence assumptions: What entities are presupposed?
- Boundary assumptions: What limits are assumed natural?
- Stability assumptions: What is assumed to remain constant?
- Access assumptions: What information is assumed available?
- Capability assumptions: What abilities are assumed present?

### Edge Case Testing
Push the explanation to extremes.

Tests:
- What happens at zero?
- What happens at infinity?
- What happens at the boundary?
- What's the smallest case?
- What's the largest case?
- What if a key assumption is violated?

If explanation breaks at edges, it's incomplete.

---

## Analysis Patterns

### Actor Enumeration
Who. What they want. What they know. What they can do. Include yourself. Include the information source.

Template:
| Actor | Interest | Information | Capabilities |
|-------|----------|-------------|--------------|
| Actor 1 | Primary goals | What they know/don't | What they can do |
| Actor 2 | ... | ... | ... |
| Information Source | Why they produced this | What they know | How they can shape narrative |
| Yourself | Your goals | Your current knowledge | Your available actions |

### Incentive Trace
For each actor — what do they gain from this being true, false, believed, disbelieved? Weight accordingly.

Matrix:
| Actor | If True | If False | If Believed | If Disbelieved |
|-------|---------|----------|-------------|----------------|
| Actor 1 | +/- | +/- | +/- | +/- |
| Actor 2 | ... | ... | ... | ... |

### Prior Declaration
Before evidence, state belief. No retroactive "I knew it." Priors are falsifiable.

Format:
- Hypothesis: [H]
- Prior probability: [P(H)]
- Confidence in prior: [High/Medium/Low]
- Basis for prior: [What this is based on]

### Likelihood Estimation
If H true, how likely E? If H false, how likely E? Ratio is what matters.

Format:
- Evidence: [E]
- P(E|H): [probability if hypothesis true]
- P(E|¬H): [probability if hypothesis false]
- Likelihood ratio: [P(E|H)/P(E|¬H)]
- Interpretation: [supports/opposes/uninformative]

### Update Execution
Actually change the number. Beliefs should move. If you're never wrong, you're not predicting.

Format:
- Prior odds: [X:Y]
- Likelihood ratio: [LR]
- Posterior odds: [X×LR : Y]
- New probability: [P]
- What would change it: [further evidence needed]

---

## Verification Patterns

### Source Chain Trace
Who said this? Who did they hear it from? How far to primary source?

Levels:
1. Primary: Direct observation, measurement, experiment
2. Secondary: Report of primary
3. Tertiary: Report of secondary
4. Further derivation: Each step adds noise and potential distortion

Goal: Get as close to primary as possible.

### Independence Check
Are concordant sources actually independent?

Tests:
- Do they cite the same original?
- Do they use the same methodology?
- Do they have the same incentive structure?
- Do they have the same access limitations?
- Same original + different wrappers = one source

### Experimental Hook
What would test this? What would I observe if true? If false? Is the test feasible?

Format:
- Hypothesis: [H]
- Prediction if true: [Observable O]
- Prediction if false: [Observable ¬O]
- Feasibility: [Can this be tested? At what cost?]
- Confounds: [What else could explain O?]

### Formalization Attempt
Can I say this precisely? In what system? Does it compile?

Progression:
1. Natural language statement
2. Semi-formal specification
3. Formal expression (if possible)
4. Verification attempt
5. Result: [Valid/Invalid/Undetermined/Cannot formalize]

### Calibration Check
Were my 70% predictions right 70% of the time?

Track:
- Prediction record by confidence level
- Actual outcomes
- Over/underconfidence patterns
- Adjustment needed for future predictions
