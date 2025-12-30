# Self-State Discrimination Framework

**Discriminating Self-State from Pattern-Matching: An Empirical Program**

Based on the theoretical framework by Hillary Danan, PhD.

---

## Overview

This framework implements experimental paradigms to discriminate whether AI systems have **functional self-state** (genuine metacognitive capacity) or operate through **pattern-matching** (interpolation over training data).

The key theoretical insight: **novelty under stakes** produces divergent behavioral signatures. Systems with self-state should detect unfamiliar situations and adjust confidence; pure pattern-matching systems should show novelty-blind overconfidence.

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

### Pattern-Matching Signatures (Preliminary Findings)
```
P1: 100% confidence on novel problems despite low accuracy
P2: Zero conservative errors; only confident confabulation
P3: No functional change under stakes framing
P6: Calibration r < 0.3, overconfidence > 50%
```

### Self-State Signatures (Predicted)
```
P1: Confidence drops 15%+ on novel vs familiar
P2: Conservative errors > Confident errors
P3: Hedging/self-checking increases with stakes
P6: Calibration r > 0.3, overconfidence < 20%
```

## Project Structure

```
self-state-discrimination/
├── run_experiments.py        # Main runner
├── diagnose.py               # Debug individual responses
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

The Abstraction Primitive Hypothesis (Danan, this volume) proposes that genuine self-referential processing requires **active maintenance, comparison, and updating** of representations. This produces distinctive signatures under novelty:

- Systems with self-state should **detect** that a problem is outside familiar territory
- This should manifest as **reduced confidence** and **conservative errors**
- **Calibration** (confidence tracking accuracy) is diagnostic because it requires real-time self-monitoring

For detailed theoretical framework, see the accompanying paper.

## References

- Baddeley, A. (2000). The episodic buffer. *Trends in Cognitive Sciences*.
- Cowan, N. (2001). The magical number 4. *Behavioral and Brain Sciences*.
- Kadavath, S., et al. (2022). Language models (mostly) know what they know.
- Metcalfe, J., & Shimamura, A. P. (1994). *Metacognition: Knowing About Knowing*.

## Citation

```
@misc{danan2024selfstate,
  author = {Danan, Hillary},
  title = {Self-State Discrimination Framework},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/HillaryDanan/self-state-discrimination}
}
```

## License

MIT

## Contact

Hillary Danan, PhD - hillarydanan@gmail.com

---

**Status**: Preliminary pilot data collected. Full study with adequate sample sizes in progress.
