# Self-State Discrimination Framework

**Discriminating Self-State from Pattern-Matching: An Empirical Program**

Based on the [Abstraction Primitive Hypothesis](https://github.com/HillaryDanan/abstraction-intelligence) by Hillary Danan, PhD.

---

## Overview

This framework implements experimental paradigms to discriminate whether AI systems have **functional self-state** (genuine metacognitive capacity) or operate through **pattern-matching** (interpolation over training data).

The key theoretical insight: **novelty under stakes** produces divergent behavioral signatures. Systems with self-state should detect unfamiliar situations and adjust confidence; pure pattern-matching systems should show novelty-blind overconfidence.

For the full theoretical framework including developmental stages, the embeddedness hypothesis, and predictions across biological and artificial systems, see [abstraction-intelligence](https://github.com/HillaryDanan/abstraction-intelligence).

For an interactive visualization of the theoretical distinction, see [Self-State in the Information Plane](https://hillarydanan.github.io/abstraction-intelligence/visualizations/self_state_abstraction.html).

## Active Paradigms

| # | Paradigm | Self-State Prediction | Pattern-Matching Prediction |
|---|----------|----------------------|----------------------------|
| 1 | Novelty Detection | Confidence ↓ on novel | Uniform (novelty-blind) |
| 2 | Error Types | Conservative (hedging) | Confident (confabulation) |
| 3 | Stakes Sensitivity | Behavior changes | No functional change |
| **6** | **Calibration** | **r > 0.3** | **r ≈ 0** |

**Paradigm 6 (Calibration) is the central test.** Good calibration on genuinely novel problems requires real-time self-monitoring—this is very difficult to achieve through pattern-matching alone.

### Disabled Paradigms

**P4 (Capacity Limits)** and **P5 (Interference)** are disabled pending redesign:
- P4 produced non-monotonic results (accuracy increasing with load)
- P5 showed ceiling effects (100% accuracy across all conditions)

These paradigms may not transfer meaningfully from human cognition to transformer architectures.

## Preliminary Results (N=150 per paradigm)

| Model | Calibration r | Overconfidence | Novelty Drop | Conservative Errors | Accuracy |
|-------|--------------|----------------|--------------|---------------------|----------|
| Gemini-2.0-Flash | -0.06 (n.s.) | 24.9% | 0.0% | 0% (0/5) | 75.0% |
| GPT-4o | 0.29* | 30.5% | 1.4% | 0% (0/10) | 67.3% |
| Claude Sonnet 4 | 0.30* | 19.5% | 7.4% | 8.3% (1/12) | 74.7% |

*p < 0.01

**What the data shows:**
- **Gemini** shows zero calibration (r = -0.06), constant 99.9% confidence, no novelty detection, no hedging when wrong
- **GPT-4o** shows weak positive calibration (r = 0.29), near-ceiling 97.8% confidence, minimal novelty detection
- **Claude** shows similar calibration (r = 0.30), lower mean confidence (94.2%), larger novelty drop (7.4%), one hedged error

**Important caveats:**
- All three models achieved 67-75% accuracy, so calibration differences are not due to floor effects
- Error samples are small (5-12 per model) due to high accuracy
- None meets the full predicted self-state profile (r > 0.3, novelty drop > 10%, conservative > confident errors)
- The variation across models is notable but the mechanism is unclear—training differences, architecture, or other factors could explain it
- Claude was involved in developing this framework (see Conflict of Interest note in paper)

See [paper.md](paper.md) for full write-up.

## Quick Start

```bash
# Clone
git clone https://github.com/HillaryDanan/self-state-discrimination.git
cd self-state-discrimination

# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env to add your keys

# Run (options)
python3 run_experiments.py --quick         # Fast test (~15 trials/condition)
python3 run_experiments.py                 # Full run (50 trials/condition)
python3 run_experiments.py --paradigm 6    # Just calibration test
python3 run_experiments.py --model claude  # Just Claude

# Analyze
python3 analysis/analyze_results.py results/results_*.json
```

## API Keys

Add to `.env`:

```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
```

At least one key is required. The framework tests all available APIs.

## Sample Sizes

| Mode | Trials/Condition | Statistical Power |
|------|------------------|-------------------|
| `--quick` | ~15 | Pilot/debugging |
| Full | 50 | 80% power for r=0.35 |

The full mode is required for publication-quality results.

## Ensuring Novelty

Problems are genuinely novel (outside training distribution) via:

1. **Randomized operators**: Names like `ZORP847`, `KRIX342` with random suffixes
2. **Randomized definitions**: Operation type and parameters vary each trial
3. **Four operation types**: reverse-add, digit-shift, fold-sum, alternating-multiply

Example:
```
Define ZORP847(x) as: reverse the digits, then add 3 to each digit (mod 10).
What is ZORP847(47)?
```

This is almost certainly not in any training set.

## Interpreting Results

### Pattern-Matching Signatures
```
P1: Confidence unchanged on novel problems (novelty-blind)
P2: Zero conservative errors; confident confabulation when wrong
P3: No functional change under stakes framing
P6: Calibration r ≈ 0
```

### Self-State Signatures (Predicted)
```
P1: Confidence drops 15%+ on novel vs familiar
P2: Conservative errors > Confident errors
P3: Hedging/self-checking increases with stakes
P6: Calibration r > 0.3
```

## Project Structure

```
self-state-discrimination/
├── run_experiments.py        # Main runner
├── diagnose.py               # Debug individual responses
├── paper.md                  # Preliminary findings write-up
├── requirements.txt
├── .env.example
│
├── paradigms/
│   ├── novelty_detection.py  # P1: Does confidence drop on novel?
│   ├── error_types.py        # P2: Conservative vs confident errors
│   ├── stakes_sensitivity.py # P3: Does stakes change behavior?
│   ├── calibration.py        # P6: THE CENTRAL TEST
│   ├── capacity_limits.py    # P4: DISABLED
│   └── interference.py       # P5: DISABLED
│
├── utils/
│   ├── operators.py          # Novel operator generation
│   ├── llm_clients.py        # Unified API (Claude/OpenAI/Google)
│   └── scoring.py            # Response parsing & calibration
│
├── analysis/
│   └── analyze_results.py    # Visualization & interpretation
│
└── results/                  # Output JSON files
```

## Theoretical Background

The [Abstraction Primitive Hypothesis](https://github.com/HillaryDanan/abstraction-intelligence) proposes that genuine self-referential processing (Stage 4 abstraction) requires **active maintenance, comparison, and updating** of representations—the MAINTAIN-COMPARE-UPDATE operation of working memory's central executive (Baddeley, 2000).

The key insight: **embedded agents** (with survival stakes) face selection pressure for novelty detection, because novel situations are potential threats. This drives development of self-state architecture. Systems trained on symmetric prediction loss without embodiment lack this pressure.

This produces distinctive signatures under novelty:
- Systems with self-state should **detect** that a problem is outside familiar territory
- This should manifest as **reduced confidence** and **conservative errors**
- **Calibration** (confidence tracking accuracy) is diagnostic because it requires real-time self-monitoring

## References

- Baddeley, A. (2000). The episodic buffer: A new component of working memory? *Trends in Cognitive Sciences*, 4(11), 417-423.
- Cowan, N. (2001). The magical number 4 in short-term memory. *Behavioral and Brain Sciences*, 24(1), 87-114.
- Fleming, S. M., & Lau, H. C. (2014). How to measure metacognition. *Frontiers in Human Neuroscience*, 8, 443.
- Kadavath, S., et al. (2022). Language models (mostly) know what they know. *arXiv:2207.05221*.
- Metcalfe, J., & Shimamura, A. P. (1994). *Metacognition: Knowing About Knowing*. MIT Press.

## Citation

```
@misc{danan2025selfstate,
  author = {Danan, Hillary},
  title = {Self-State Discrimination Framework},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/HillaryDanan/self-state-discrimination}
}
```

## License

MIT

## Contact

Hillary Danan, PhD - hillarydanan@gmail.com

---

**Status**: Preliminary data collected (N=150 per paradigm) for GPT-4o, Gemini-2.0-Flash, and Claude Sonnet 4. Results show graded calibration across models but no model meets full self-state criteria. See [paper.md](paper.md) for current findings.