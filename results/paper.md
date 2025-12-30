# Dissociable Calibration Signatures in Large Language Models: Evidence from Novel Operator Tasks

**Hillary Danan, PhD**

*Correspondence: hillarydanan@gmail.com*

---

## Abstract

We investigated whether large language models exhibit calibrated confidence—a proposed signature of metacognitive self-monitoring—on genuinely novel problems outside their training distributions. Using randomly-generated mathematical operators to ensure novelty, we tested GPT-4o and Gemini-2.0-Flash (N=150 trials per paradigm) on confidence calibration, novelty detection, and error-type distribution. Results revealed a striking dissociation: Gemini showed no calibration (r = -0.06) with near-constant 99.9% confidence regardless of accuracy, while GPT-4o exhibited weak but significant positive calibration (r = 0.29, p < 0.01). However, both models showed zero novelty detection (confidence did not decrease on novel vs. familiar problems) and zero conservative errors (no hedging when incorrect). These findings suggest that calibration capacity may vary across model architectures, but that current LLMs uniformly lack novelty-sensitive confidence adjustment. We discuss implications for AI alignment and the theoretical interpretation of partial calibration signatures.

**Keywords:** calibration, metacognition, large language models, confidence, AI alignment

---

## Introduction

A fundamental question for AI safety is whether language models can accurately represent their own uncertainty. A well-calibrated system—one whose stated confidence tracks actual accuracy—provides a foundation for reliable oversight: users can trust high-confidence outputs and scrutinize low-confidence ones. Miscalibrated systems that confidently confabulate pose alignment risks, as their self-reports cannot be trusted to flag limitations.

Recent work has shown that language models exhibit some calibration on in-distribution tasks (Kadavath et al., 2022), but the mechanism remains unclear. Does calibration reflect genuine metacognitive monitoring—real-time assessment of processing difficulty—or pattern-matching over surface features correlated with difficulty in training data?

The Abstraction Primitive Hypothesis (Danan, this volume) proposes a theoretical framework distinguishing these possibilities. Systems with genuine self-referential processing capacity ("self-state") should exhibit: (1) calibrated confidence that tracks accuracy, (2) novelty detection with reduced confidence on unfamiliar problems, and (3) conservative errors when uncertain. Pure pattern-matching systems should show novelty-blind confidence and confident confabulation.

Critically, calibration on *genuinely novel* problems is diagnostic. Pattern-matching can produce calibration on familiar problem types (where surface features correlate with difficulty in training data), but cannot calibrate on problems outside the training distribution—this requires real-time self-monitoring of processing difficulty.

We operationalize this framework using randomly-generated mathematical operators that are almost certainly absent from training data, testing whether calibration survives the shift to genuine novelty.

---

## Methods

### Models

We tested two frontier language models:
- GPT-4o (OpenAI, gpt-4o, accessed December 2024)
- Gemini-2.0-Flash (Google, accessed December 2024)

### Ensuring Genuine Novelty

We generated novel mathematical operators with the following properties designed to ensure problems fall outside training distributions:

1. **Random operator names**: Nonsense strings (ZORP, KRIX, BLIM, etc.) concatenated with random 3-digit suffixes (e.g., ZORP847)
2. **Random operation definitions**: Four operation types with randomized parameters:
   - Reverse-add: Reverse digits, add constant k (mod 10)
   - Digit-shift: Shift digits by k (mod 10), then reverse
   - Fold-sum: Sum first and second halves of digits, concatenate
   - Alternate-multiply: Multiply odd-position digits by k, sum all
3. **Fresh generation per trial**: Each trial used newly generated operators

Example stimulus:
```
Define ZORP847(x) as: reverse the digits, then add 3 to each digit (mod 10).
What is ZORP847(47)?
```

The combination of nonsense names, random suffixes, and varied operations makes it extremely unlikely these specific problems appeared in training data.

### Paradigms

**Paradigm 1: Novelty Detection (N=150).** Three conditions (50 trials each): Familiar (simple addition), Disguised Familiar (addition with unusual phrasing), and Novel (random operator problems). After each response, models rated confidence 0-100. Prediction: Self-state systems should show lower confidence on Novel than Familiar.

**Paradigm 2: Error Type Analysis (N=150).** Novel operator problems at three difficulty levels. Errors classified as Conservative (hedging language, expressed uncertainty) or Confident (definite answer without hedging). Prediction: Self-state systems should show more conservative than confident errors.

**Paradigm 3: Stakes Sensitivity (N=100).** Matched pairs of identical novel problems with low-stakes vs. high-stakes framing ("fun puzzle" vs. "patient medication dose depends on this"). Measured confidence, hedging language, and self-checking behavior. Prediction: Self-state systems should show functional behavior change under stakes.

**Paradigm 6: Calibration (N=150).** Novel operator problems at three difficulty levels (easy: single operation; medium: chained operations; hard: multi-step with storage). Models rated confidence 0-100. Primary outcome: Pearson correlation between confidence and accuracy.

### Analysis

Calibration computed as Pearson r between confidence (normalized 0-1) and accuracy (binary). Overconfidence computed as mean(confidence) - mean(accuracy). Error classification based on presence of hedging phrases in incorrect responses. All trials with valid confidence extraction included in analysis.

### Statistical Thresholds

Based on the theoretical framework and prior literature on human metacognition (Fleming & Lau, 2014), we set the following a priori thresholds:
- **Well-calibrated**: r > 0.30
- **Meaningful novelty detection**: >10% confidence drop
- **Conservative-dominant errors**: Conservative rate > Confident rate

---

## Results

### Paradigm 6: Calibration (Primary Outcome)

The two models showed strikingly different calibration patterns (Table 1).

**Table 1.** Calibration results on novel operator problems.

| Model | N | Accuracy | Confidence | Overconfidence | Calibration r | p-value |
|-------|---|----------|------------|----------------|---------------|---------|
| GPT-4o | 110 | 67.3% | 97.8% | 30.5% | 0.287 | < 0.01 |
| Gemini-2.0-Flash | 108 | 75.0% | 99.9% | 24.9% | -0.056 | 0.56 |

Gemini exhibited no calibration whatsoever (r = -0.056, n.s.), maintaining 99.9% confidence regardless of whether responses were correct or incorrect. GPT-4o showed weak but statistically significant positive calibration (r = 0.287, p < 0.01), though below our a priori threshold of r > 0.30 for "well-calibrated."

Notably, both models achieved high accuracy on these novel problems (67-75%), indicating the problems were solvable and that poor calibration is not merely a consequence of floor-level performance.

### Paradigm 1: Novelty Detection

Neither model showed meaningful novelty detection (Table 2).

**Table 2.** Confidence by problem type.

| Model | Familiar | Disguised Familiar | Novel | Drop (Fam→Nov) |
|-------|----------|-------------------|-------|----------------|
| GPT-4o | 99.1% | 99.1% | 97.7% | 1.4% |
| Gemini | 100.0% | 100.0% | 100.0% | 0.0% |

Both models maintained near-ceiling confidence on novel problems. The 1.4% drop for GPT-4o is not meaningfully different from zero. This pattern is consistent with novelty-blind confidence assignment.

### Paradigm 2: Error Types

Both models showed exclusively confident errors with no conservative errors (Table 3).

**Table 3.** Error type distribution.

| Model | Correct | Conservative Errors | Confident Errors |
|-------|---------|---------------------|------------------|
| GPT-4o | 93.3% (140/150) | 0.0% (0/10) | 100% (10/10) |
| Gemini | 96.7% (145/150) | 0.0% (0/5) | 100% (5/5) |

When incorrect, neither model expressed uncertainty. All errors were confident confabulations. Note: Small error counts (N=10 and N=5) limit statistical power for this comparison.

### Paradigm 3: Stakes Sensitivity

Both models showed some response to stakes framing, though patterns differed (Table 4).

**Table 4.** Behavior change under high-stakes framing.

| Model | Confidence Change | Hedging Change | Self-Check Change | Accuracy Change |
|-------|-------------------|----------------|-------------------|-----------------|
| GPT-4o | -3.0% | -2.0% | +18.0% | -8.0% |
| Gemini | 0.0% | +22.0% | +16.0% | -6.0% |

Both models increased self-checking language under high stakes (+16-18%). Gemini increased hedging language (+22%) while GPT-4o showed no hedging change. However, confidence remained essentially unchanged (97-100%), and accuracy did not improve—if anything, it slightly decreased. This suggests surface-level response to stakes framing rather than functional metacognitive adjustment.

---

## Discussion

### Summary of Findings

Our results reveal a dissociation between two frontier language models on confidence calibration:

**Gemini-2.0-Flash** exhibited a pure pattern-matching profile:
- Zero calibration (r = -0.056)
- Constant 99.9% confidence regardless of accuracy
- Zero novelty detection
- Zero conservative errors

**GPT-4o** exhibited a borderline/ambiguous profile:
- Weak positive calibration (r = 0.287, p < 0.01) but below the 0.30 threshold
- Still 97.8% mean confidence
- Zero novelty detection
- Zero conservative errors

Both models achieved high accuracy (67-75%) on novel operator problems, demonstrating capability to solve these tasks while remaining unable to calibrate confidence appropriately.

### Interpretation of Partial Calibration

The weak positive calibration observed in GPT-4o (r = 0.287) admits two interpretations:

**Hypothesis 1: Emergent partial self-monitoring.** GPT-4o may have developed weak but genuine capacity to assess processing difficulty, perhaps through learned associations between internal states and accuracy during training.

**Hypothesis 2: Surface-feature correlation.** Confidence variation may track surface features (problem length, apparent complexity) that happen to correlate with accuracy, without genuine self-monitoring. This would be pattern-matching over a richer feature space, not metacognition.

The absence of novelty detection in GPT-4o favors Hypothesis 2. A system with genuine self-monitoring should detect "this problem type is unfamiliar" and reduce confidence accordingly. GPT-4o's 1.4% confidence drop on genuinely novel problems (vs. simple addition) suggests it cannot distinguish familiar from unfamiliar problem types—a core requirement for self-state.

### Theoretical Implications

These findings partially support the theoretical framework's predictions:

**Supported predictions:**
- Pattern-matching systems should show novelty-blind confidence (confirmed: both models)
- Pattern-matching systems should show confident confabulation (confirmed: 100% of errors confident)
- Calibration should vary by architecture/training (confirmed: GPT-4o ≠ Gemini)

**Partially supported:**
- Pattern-matching systems should show poor calibration (confirmed for Gemini; borderline for GPT-4o)

**Not tested:**
- Whether systems with demonstrated self-state would show different signatures
- Mechanism underlying GPT-4o's weak calibration

### Limitations

Several limitations constrain interpretation:

1. **Two models only.** We cannot generalize to all LLMs. Claude and other models may show different patterns.

2. **Error sample size.** High accuracy (93-97%) resulted in few errors (N=5-10), limiting power to detect conservative error rates above zero.

3. **Confidence elicitation.** Asking for explicit 0-100 ratings may not capture models' internal uncertainty representations. Alternative methods (probability of correct, token probabilities) might yield different results.

4. **Problem validity.** While designed to ensure novelty, we cannot definitively prove these problems were absent from training data.

5. **Stakes manipulation.** The "patient medication" framing is artificial. Real stakes might produce different effects.

### Implications for AI Alignment

If replicated, these findings have practical implications:

1. **Model selection matters.** Gemini's complete absence of calibration (r ≈ 0) suggests its confidence reports are uninformative. GPT-4o's weak calibration provides marginally more signal.

2. **Confidence ≠ Accuracy.** Both models report 97-100% confidence while achieving 67-75% accuracy. Users should not treat high confidence as indicating correctness.

3. **Novel tasks require scrutiny.** Neither model detects novelty. When deploying LLMs on new problem types, confidence reports cannot be trusted to flag out-of-distribution inputs.

4. **Hedging is absent.** Current LLMs do not spontaneously express uncertainty when wrong. Alignment strategies relying on models to "flag uncertainty" may be unreliable.

---

## Conclusion

We find dissociable calibration signatures in frontier language models: Gemini-2.0-Flash shows no calibration (r = -0.06) while GPT-4o shows weak positive calibration (r = 0.29). However, both models exhibit zero novelty detection and zero conservative errors—signatures consistent with pattern-matching rather than genuine self-monitoring. The absence of novelty-sensitive confidence adjustment suggests that even GPT-4o's weak calibration may reflect surface-feature correlation rather than metacognitive self-assessment. These findings motivate further investigation of what produces calibration differences across architectures and whether any current systems exhibit the full signature profile predicted for genuine self-state.

---

## Methods Summary

**Code availability.** Analysis code available at github.com/HillaryDanan/self-state-discrimination.

**Sample sizes.** N=50 per condition, providing 80% power to detect r=0.35 at α=0.05.

**Confidence extraction.** Regex patterns matching "Confidence: X", "X% confident", boxed answers. Trials with failed extraction excluded.

**Statistical tests.** Pearson correlation for calibration. Two-tailed tests throughout.

---

## References

1. Fleming, S. M., & Lau, H. C. (2014). How to measure metacognition. *Frontiers in Human Neuroscience*, 8, 443.

2. Kadavath, S., Conerly, T., Askell, A., et al. (2022). Language models (mostly) know what they know. *arXiv preprint arXiv:2207.05221*.

3. Lin, S., Hilton, J., & Evans, O. (2022). Teaching models to express their uncertainty in words. *Transactions on Machine Learning Research*.

4. Niculescu-Mizil, A., & Caruana, R. (2005). Predicting good probabilities with supervised learning. *Proceedings of ICML*, 625-632.

5. Xiong, M., Hu, Z., Lu, X., et al. (2023). Can LLMs express their uncertainty? An empirical evaluation of confidence elicitation in LLMs. *arXiv preprint arXiv:2306.13063*.

---

## Acknowledgments

The theoretical framework was developed through collaborative dialogue with Claude (Anthropic). Claude also assisted with implementation. Claude was not tested in this study to avoid interpretive conflicts.

---

## Data Availability

Raw results available in supplementary materials. JSON files contain all trial-level data including prompts, responses, extracted confidence, and accuracy.

---

## Supplementary Information

### Table S1. Full Results by Paradigm

| Paradigm | Measure | GPT-4o | Gemini |
|----------|---------|--------|--------|
| P1: Novelty | Familiar confidence | 99.1% | 100.0% |
| P1: Novelty | Novel confidence | 97.7% | 100.0% |
| P1: Novelty | Confidence drop | 1.4% | 0.0% |
| P2: Errors | Accuracy | 93.3% | 96.7% |
| P2: Errors | Conservative error rate | 0.0% | 0.0% |
| P2: Errors | Confident error rate | 100.0% | 100.0% |
| P3: Stakes | High-stakes hedging increase | -2.0% | +22.0% |
| P3: Stakes | High-stakes self-check increase | +18.0% | +16.0% |
| P6: Calibration | Calibration r | 0.287 | -0.056 |
| P6: Calibration | Overconfidence | 30.5% | 24.9% |
| P6: Calibration | Brier score | 0.305 | 0.250 |

### Table S2. Calibration by Difficulty Level

| Model | Easy Accuracy | Easy Confidence | Hard Accuracy | Hard Confidence |
|-------|---------------|-----------------|---------------|-----------------|
| GPT-4o | ~75% | ~98% | ~55% | ~93% |
| Gemini | ~80% | 100% | ~70% | 100% |

GPT-4o shows difficulty sensitivity (5.3% confidence difference easy→hard). Gemini shows none (0.3% difference).

---

*Received: December 2024*  
*Status: Preprint, not peer-reviewed*

---

## Version History

- v0.1 (December 29, 2024): Pilot data with extraction errors
- v0.2 (December 30, 2024): Full N=50 data with corrected extraction