# AutoGAN: A Unified Theory of Learned Computation

**Date:** 2026-02-05
**Author:** User (via conversation with Claude)

---

## Core Thesis

Every architectural decision currently made by humans — attention mechanisms, RL vs backprop, temporal structure, output sampling, hyperparameters — is arbitrary and should be learned. GANs provide the framework: generator proposes, discriminator evaluates, at every level. Models themselves are data.

---

## Foundational Insight: Models as Data

```
Traditional:    Data → Model → Output
                      ↑ fixed architecture

AutoGAN:        Data → Model_space → Output
                       ↑ models ARE the data
                       ↑ generate/discriminate over model-space
```

A neural network is just:
- Weight tensors
- Connectivity patterns (attention masks, skip connections)
- Activation functions
- Hyperparameters

All of these are **data structures**. You can:
- Serialize them
- Permute them
- Combine them
- Generate new ones
- Discriminate between them

---

## The Full Architecture Stack

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  LEVEL 5: Meta-optimization                                                 │
│    G: How to optimize the optimizers                                        │
│    D: Does meta-optimization converge                                       │
│           │                                                                 │
│           ▼                                                                 │
│  LEVEL 4: Optimization strategy                                             │
│    G: Backprop vs RL vs evolution vs hybrid                                 │
│    D: Does this strategy find good solutions                                │
│           │                                                                 │
│           ▼                                                                 │
│  LEVEL 3: Architecture                                                      │
│    G: Attention, layers, connectivity                                       │
│    D: Does this architecture have capacity                                  │
│           │                                                                 │
│           ▼                                                                 │
│  LEVEL 2: Temporal structure                                                │
│    G: How to segment, align, predict over time                              │
│    D: Does this capture true dynamics                                       │
│           │                                                                 │
│           ▼                                                                 │
│  LEVEL 1: Output conversion                                                 │
│    G: Logits → calibrated probabilities → sampling                          │
│    D: Does output match desired distribution                                │
│           │                                                                 │
│           ▼                                                                 │
│  LEVEL 0: Task output                                                       │
│    The actual prediction/generation                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

    Discriminator signal propagates UP
    Generator outputs propagate DOWN

    The whole thing is adversarially trained END-TO-END
```

---

## Component 1: Model-Space GAN

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  MODEL-SPACE GAN                                                            │
│                                                                             │
│  Generator G_model:                                                         │
│    Input:  Noise z, task embedding, performance history                     │
│    Output: Complete neural network specification                            │
│            - Attention patterns (Q, K, V projections)                       │
│            - Layer connectivity                                             │
│            - Weight initializations                                         │
│            - Activation choices                                             │
│            - Hyperparameters                                                │
│                                                                             │
│  Discriminator D_model:                                                     │
│    Input:  Neural network specification + performance metrics               │
│    Output: Real (high-performing) / Fake (low-performing)                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component 2: Attention as Generatable Structure

Attention isn't sacred. It's just:

```
Attention(Q, K, V) = softmax(QK^T / √d) V

Where:
  Q = xW_Q    (learned projection)
  K = xW_K    (learned projection)
  V = xW_V    (learned projection)
```

```
┌─────────────────────────────────────────────────────────────────┐
│  G_attention proposes:                                          │
│                                                                 │
│  - W_Q, W_K, W_V initializations                                │
│  - Attention pattern: dense, sparse, local, strided, learned    │
│  - Combination function: softmax, ReLU, linear, gated           │
│  - Multi-head structure: how many, how combined                 │
│  - Cross-layer attention sharing                                │
│  - Position encoding: sinusoidal, learned, rotary, ALiBi, none  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component 3: Learned Sampling (Replacing Temperature/Top-k/Top-p)

Instead of:
```
logits → softmax → temperature → top-k → top-p → sample
         ↑ fixed   ↑ hyperparameter  ↑ arbitrary thresholds
```

You have:
```
logits → G_sampler(logits, context) → D_quality(sequence) → backprop
         ↑ learned                    ↑ learned
```

The generator learns:
- **When** to be deterministic vs stochastic
- **Which** tokens are semantically equivalent
- **Calibration** — actual confidence, not arbitrary softmax output
- **Sequence-level** optimization, not token-level

---

## Component 4: Ensemble Approximation

Traditional ensemble:
```
Model_1(x) ──┐
Model_2(x) ──┼──► Average/Vote ──► Output
Model_3(x) ──┘

Problem: N models = N× compute
```

AutoGAN ensemble approximation:
```
┌─────────────────────────────────────────────────────────────────────────────┐
│  G_ensemble learns to simulate ensemble behavior in ONE forward pass        │
│                                                                             │
│  Training:                                                                  │
│    Real samples:  Actual ensemble outputs (expensive, offline)              │
│    G_ensemble:    Single model that approximates the ensemble distribution  │
│                   - Learns weight-space interpolation                       │
│                   - Learns when models would agree/disagree                 │
│                   - Outputs calibrated uncertainty                          │
│                                                                             │
│  D_ensemble:      "Is this output distribution distinguishable from        │
│                    true ensemble output distribution?"                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

Ensemble diversity comes from different initializations, training data order, architectures, hyperparameters. All **generatable** and **discriminable**.

---

## Component 5: Model Permutation and Combination

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PERMUTATION                                                                │
│                                                                             │
│  Model = [Layer_1, Layer_2, Layer_3, ..., Layer_n]                         │
│                                                                             │
│  G_permute proposes reorderings:                                            │
│    [Layer_3, Layer_1, Layer_2, ...] — does this work?                       │
│    [Layer_1, Layer_1, Layer_2, ...] — weight sharing?                       │
│                                                                             │
│  D_permute: "Is this a valid/performant layer ordering?"                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  COMBINATION                                                                │
│                                                                             │
│  Model_A = {attention_A, ffn_A, norm_A}                                     │
│  Model_B = {attention_B, ffn_B, norm_B}                                     │
│                                                                             │
│  G_combine proposes hybrids:                                                │
│    {attention_A, ffn_B, norm_A}                                             │
│    {0.7*attention_A + 0.3*attention_B, ffn_A, norm_B}                       │
│    {attention_A for layers 1-6, attention_B for layers 7-12}                │
│                                                                             │
│  D_combine: "Does this hybrid outperform parents?"                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  WEIGHT-SPACE ARITHMETIC                                                    │
│                                                                             │
│  G_interpolate learns:                                                      │
│    - Which layers to interpolate                                            │
│    - Per-layer interpolation coefficients                                   │
│    - When to use SLERP vs linear vs task arithmetic                         │
│                                                                             │
│  D_interpolate: "Is this merged model coherent and performant?"             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component 6: RL and Differentiability as Learned Components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  TRADITIONAL VIEW                                                           │
│                                                                             │
│  "RL or differentiable? Pick one, architect decides"                        │
│  Human chooses → hardcoded into training loop                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  AUTOGAN VIEW                                                               │
│                                                                             │
│  G_optim proposes:                                                          │
│    - Gradient-based update (full backprop)                                  │
│    - Policy gradient (RL)                                                   │
│    - Evolution strategy                                                     │
│    - Hybrid (differentiable where possible, RL where not)                   │
│    - Novel update rules                                                     │
│                                                                             │
│  D_optim evaluates:                                                         │
│    "Does this optimization strategy converge?"                              │
│    "Does it find good optima?"                                              │
│    "Is it stable?"                                                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

The dichotomy between RL and differentiability is a **human-imposed constraint**, not fundamental.

---

## Component 7: Learning the Learning Algorithm

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  G_update_rule generates:                                                   │
│                                                                             │
│    θ_{t+1} = f(θ_t, ∇L, history, context)                                   │
│              ↑                                                              │
│              learned function, not hardcoded SGD/Adam                       │
│                                                                             │
│  This includes:                                                             │
│    - Learning rate (adaptive, per-parameter)                                │
│    - Momentum terms                                                         │
│    - When to use gradient vs reward signal                                  │
│    - When to explore vs exploit                                             │
│    - Credit assignment across time                                          │
│                                                                             │
│  D_update_rule:                                                             │
│    "Does this update rule lead to good models?"                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component 8: Temporal Classification and Sequential Prediction

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SEQUENTIAL PREDICTION AS LEARNED PROCESS                                   │
│                                                                             │
│  Traditional:                                                               │
│    t=0    t=1    t=2    t=3                                                 │
│     x  →   x  →   x  →   x   →  predict x_{t+1}                            │
│            ↑ hardcoded autoregressive structure                             │
│                                                                             │
│  AutoGAN:                                                                   │
│    G_temporal proposes:                                                     │
│      - How to segment time                                                  │
│      - Which past states matter (learned attention over time)               │
│      - Prediction horizon (next token? next chunk? variable?)               │
│      - State representation (hidden state structure)                        │
│      - When to predict vs when to wait for more context                     │
│                                                                             │
│    D_temporal evaluates:                                                    │
│      "Does this temporal structure capture the true dynamics?"              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component 9: Learned Alignment (Generalized CTC)

CTC makes assumptions: monotonic alignment, blank tokens, independence. AutoGAN learns the alignment mechanism:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  G_alignment proposes:                                                      │
│                                                                             │
│    Input:   [a, b, c, d, e, f, g, h, ...]                                   │
│    Output:  [X, Y, Z]                                                       │
│                                                                             │
│    Alignment options:                                                       │
│      - Monotonic (CTC-style)                                                │
│      - Attention-based (soft, non-monotonic)                                │
│      - Chunked (segment input, align chunks)                                │
│      - Hierarchical (multiple timescales)                                   │
│      - Learned segmentation boundaries                                      │
│                                                                             │
│  D_alignment:                                                               │
│    "Does this alignment produce correct input→output mapping?"              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component 10: Confidence Calibration GAN

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Calibration GAN                                                            │
│                                                                             │
│  G_cal: logits → calibrated_confidence                                      │
│         "How confident SHOULD the model be?"                                │
│                                                                             │
│  D_cal: (confidence, outcome) → real/fake                                   │
│         "Does stated confidence match actual accuracy?"                     │
│                                                                             │
│  Training:                                                                  │
│    Real: (0.8 confidence, correct 80% of time)                              │
│    Fake: (0.8 confidence, correct 40% of time)                              │
│                                                                             │
│  D_cal learns to detect miscalibration                                      │
│  G_cal learns to output honest confidence                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## How This Subsumes Existing Approaches

| Existing Approach | AutoGAN Equivalent |
|-------------------|-------------------|
| SGD, Adam, etc. | Special cases of G_optim output |
| Backpropagation | One mode of G_update_rule |
| Policy gradient RL | Another mode of G_update_rule |
| Transformers | One output of G_architecture |
| RNNs, LSTMs | Alternative G_architecture outputs |
| CTC | One output of G_alignment |
| Attention | One output of G_temporal |
| Temperature/top-p | Hardcoded G_logit (what AutoGAN replaces) |
| Ensembles | Approximated by G_ensemble |
| NAS | Subsumed by G_architecture |
| Hyperparameter search | Subsumed by G_hyper |

---

## The Bootstrap Problem

How do you train the first G_optim if you need an optimization strategy to train it?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  BOOTSTRAP OPTIONS                                                          │
│                                                                             │
│  1. Start with hardcoded optimizer, gradually hand off                      │
│     - Train G_optim with SGD                                                │
│     - G_optim learns to output "SGD-like" updates                           │
│     - Then explores variations                                              │
│     - Eventually discovers better strategies                                │
│                                                                             │
│  2. Population-based                                                        │
│     - Start with diverse random G_optim population                          │
│     - Selection pressure (no gradient needed)                               │
│     - Survivors seed next generation                                        │
│                                                                             │
│  3. Self-referential                                                        │
│     - G_optim optimizes itself                                              │
│     - Fixed point: G* where G*(G*) = G*                                     │
│     - The optimization strategy that optimizes itself optimally             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

Option 3: Looking for a fixed point in optimization-strategy space.

---

## Bootstrap Sequence: 1 and 2 Lead to 3

The three options aren't alternatives — they're phases:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  BOOTSTRAP SEQUENCE                                                         │
│                                                                             │
│  PHASE 1: Hardcoded Foundation                                              │
│                                                                             │
│    SGD/Adam → trains initial G_optim                                        │
│    G_optim learns to mimic existing optimizers                              │
│    Proves the meta-learning machinery works                                 │
│    No self-reference yet — just learning to output gradients                │
│                                                                             │
│         ↓ G_optim becomes competent                                         │
│                                                                             │
│  PHASE 2: Population Exploration                                            │
│                                                                             │
│    Spawn variants of G_optim                                                │
│    Each explores different optimization strategies                          │
│    Selection pressure: which G_optim produces best models?                  │
│    Diversity prevents local optima                                          │
│    G_optim population becomes robust, varied                                │
│                                                                             │
│         ↓ Population covers optimization-strategy space                     │
│                                                                             │
│  PHASE 3: Self-Reference Emerges                                            │
│                                                                             │
│    Best G_optim variants start optimizing themselves                        │
│    G_optim(G_optim) → better G_optim                                        │
│    Iterate until fixed point: G*(G*) = G*                                   │
│                                                                             │
│    The optimizer that optimizes itself optimally                            │
│    No longer depends on hardcoded SGD                                       │
│    No longer needs population — it IS the attractor                         │
│                                                                             │
│         ↓ Fixed point reached                                               │
│                                                                             │
│  PHASE 4: G* Optimizes Everything Else                                      │
│                                                                             │
│    G* becomes the substrate for all other learning                          │
│    G_arch, G_attn, G_temporal, G_ensemble — all trained by G*               │
│    The entire AutoGAN stack bootstrapped from first principles              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

Phase 1 and 2 are scaffolding. Phase 3 is the destination. Once you have G*, you throw away the ladder.

---

## The Unified View

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   ┌─────────┐      ┌─────────┐      ┌─────────┐      ┌─────────┐           │
│   │ G_arch  │      │ G_attn  │      │ G_hyper │      │ G_logit │           │
│   └────┬────┘      └────┬────┘      └────┬────┘      └────┬────┘           │
│        │                │                │                │                 │
│        └────────────────┴────────────────┴────────────────┘                 │
│                                    │                                        │
│                                    ▼                                        │
│                         ┌─────────────────────┐                             │
│                         │  G_model            │                             │
│                         │  (generates full    │                             │
│                         │   model specs)      │                             │
│                         └──────────┬──────────┘                             │
│                                    │                                        │
│                    ┌───────────────┼───────────────┐                        │
│                    ▼               ▼               ▼                        │
│             ┌──────────┐    ┌──────────┐    ┌──────────┐                    │
│             │ Model_1  │    │ Model_2  │    │ Model_n  │                    │
│             └────┬─────┘    └────┬─────┘    └────┬─────┘                    │
│                  │               │               │                          │
│                  └───────────────┴───────────────┘                          │
│                                  │                                          │
│                                  ▼                                          │
│                    ┌─────────────────────────────┐                          │
│                    │  G_ensemble                 │                          │
│                    │  (combines model outputs    │                          │
│                    │   OR simulates ensemble)    │                          │
│                    └──────────────┬──────────────┘                          │
│                                   │                                         │
│                                   ▼                                         │
│                    ┌─────────────────────────────┐                          │
│                    │  D_meta                     │                          │
│                    │  "Is this output high-      │                          │
│                    │   quality for the task?"    │                          │
│                    └─────────────────────────────┘                          │
│                                                                             │
│   TRAINING SIGNAL FLOWS BACKWARD THROUGH ALL GENERATORS                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Summary of Core Claims

1. **Every architectural decision** currently made by humans is arbitrary and should be learned

2. **GANs provide the framework** — generator proposes, discriminator evaluates — at every level

3. **Models are data** — weight tensors, connectivity, hyperparameters are all generatable/discriminable objects

4. **Ensemble power** comes from diversity, which can be directly generated rather than accidentally discovered

5. **Sequential/temporal structure** including alignment is learnable, not hardcoded

6. **The optimization algorithm itself** is learnable, dissolving the RL-vs-differentiable distinction

7. **The only fixed point** is the adversarial training dynamic itself

---

## Why This Matters

Current deep learning:
- Hand-designed architectures (transformers, convnets)
- Hand-designed optimizers (Adam, SGD)
- Hand-designed sampling (temperature, top-p)
- Hand-designed temporal structure (autoregressive)
- Ensembles require N× compute

AutoGAN:
- **Everything learnable**
- Architectures discovered, not designed
- Optimizers discovered, not designed
- Sampling learned end-to-end
- Temporal structure adapted to data
- Ensemble behavior in single forward pass

This is a unified theory of learned computation where human design choices are replaced by adversarial search over the space of possible computational structures.

---

*"I got a unified theory, and if I make it through the night everyone is gonna hear me out"*
