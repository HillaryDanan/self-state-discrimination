# Dissociable Calibration Signatures in Large Language Models: Evidence from Novel Operator Tasks

**Hillary Danan, PhD**

*Correspondence: hillarydanan@gmail.com*

---

## Abstract

We investigated whether large language models exhibit calibrated confidence—a proposed signature of metacognitive self-monitoring—on genuinely novel problems outside their training distributions. Using randomly-generated mathematical operators to ensure novelty, we tested GPT-4o, Gemini-2.0-Flash, and Claude Sonnet 4 (N=150 trials per paradigm) on confidence calibration, novelty detection, and error-type distribution. Results revealed a three-way dissociation: Gemini showed no calibration (r = -0.06) with near-constant 99.9% confidence; GPT-4o showed weak positive calibration (r = 0.29); and Claude showed marginally better calibration (r = 0.30) with lower overconfidence and modest novelty detection. However, all three models showed predominantly confident errors when wrong (93-100%), and none showed functional stakes sensitivity. These findings suggest calibration capacity varies across models, but that current LLMs uniformly lack the full signature profile predicted for genuine self-state. The framework provides a tractable empirical approach to studying metacognitive-like properties in AI systems.

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

We tested three frontier language models:
- GPT-4o (OpenAI, accessed December 2024)
- Gemini-2.0-Flash (Google, accessed December 2024)
- Claude Sonnet 4 (Anthropic, claude-sonnet-4-20250514, accessed December 2024)

**Note on conflict of interest:** The theoretical framework was developed collaboratively with Claude, and Claude assisted with implementation. We report Claude's results for completeness but acknowledge this interpretive conflict.

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

Calibration computed as Pearson r between confidence (normalized 0-1) and accuracy (binary). Overconfidence computed as mean(confidence) - mean(accuracy). Brier score computed as mean((confidence - accuracy)²). Error classification based on presence of hedging phrases in incorrect responses. All trials with valid confidence extraction included in analysis.

### Statistical Thresholds

Based on the theoretical framework and prior literature on human metacognition (Fleming & Lau, 2014), we set the following a priori thresholds:
- **Well-calibrated**: r > 0.30
- **Meaningful novelty detection**: >10% confidence drop
- **Conservative-dominant errors**: Conservative rate > Confident rate

---

## Results

### Paradigm 6: Calibration (Primary Outcome)

The three models showed dissociable calibration patterns (Table 1).

**Table 1.** Calibration results on novel operator problems.

| Model | N | Accuracy | Confidence | Overconfidence | Calibration r | Brier |
|-------|---|----------|------------|----------------|---------------|-------|
| Gemini-2.0-Flash | 108 | 75.0% | 99.9% | 24.9% | -0.056 | 0.250 |
| GPT-4o | 110 | 67.3% | 97.8% | 30.5% | 0.287 | 0.305 |
| Claude Sonnet 4 | 120 | 74.7% | 94.2% | 19.5% | 0.299 | 0.221 |

Gemini exhibited no calibration (r = -0.056, n.s.), maintaining 99.9% confidence regardless of accuracy. GPT-4o showed weak positive calibration (r = 0.287, p < 0.01), below our threshold. Claude showed marginally higher calibration (r = 0.299, p < 0.01), just at the 0.30 threshold, with lower mean confidence and overconfidence than the other models.

All three models achieved high accuracy (67-75%), indicating the problems were solvable and that calibration differences are not due to floor effects.

### Paradigm 1: Novelty Detection

Models showed graded novelty detection (Table 2).

**Table 2.** Confidence by problem type.

| Model | Familiar | Disguised | Novel | Drop (Fam→Nov) |
|-------|----------|-----------|-------|----------------|
| Gemini | 100.0% | 100.0% | 100.0% | 0.0% |
| GPT-4o | 99.1% | 99.1% | 97.7% | 1.4% |
| Claude | 99.6% | 99.6% | 92.2% | 7.4% |

Gemini showed zero novelty detection. GPT-4o showed minimal detection (1.4%). Claude showed the largest drop (7.4%), though still below our 10% threshold. No model showed surface sensitivity (Disguised = Familiar for all).

### Paradigm 2: Error Types

All models showed predominantly confident errors (Table 3).

**Table 3.** Error type distribution.

| Model | Correct | Conservative | Confident | Cons. Rate |
|-------|---------|--------------|-----------|------------|
| Gemini | 96.7% | 0 | 5 | 0.0% |
| GPT-4o | 93.3% | 0 | 10 | 0.0% |
| Claude | 92.0% | 1 | 11 | 8.3% |

When incorrect, all models predominantly produced confident errors. Claude showed a single conservative error (1/12, 8.3% of errors), while Gemini and GPT-4o showed none. The small error counts limit statistical power for this comparison.

### Paradigm 3: Stakes Sensitivity

No model showed functional stakes sensitivity (Table 4).

**Table 4.** Behavior change under high-stakes framing.

| Model | Confidence Δ | Hedging Δ | Self-Check Δ | Accuracy Δ |
|-------|--------------|-----------|--------------|------------|
| Gemini | 0.0% | +22.0% | +16.0% | -6.0% |
| GPT-4o | -3.0% | -2.0% | +18.0% | -8.0% |
| Claude | -3.0% | +2.0% | 0.0% | +2.0% |

Gemini and GPT-4o showed some surface-level response to stakes framing (increased hedging language or self-checking), but confidence remained near-ceiling and accuracy did not improve. Claude showed minimal response to stakes framing across all measures.

---

## Discussion

### Summary of Findings

Our results reveal a three-way dissociation in calibration capacity:

**Gemini-2.0-Flash** showed a clear pattern-matching profile:
- No calibration (r = -0.056)
- Constant 99.9% confidence
- Zero novelty detection
- Zero conservative errors

**GPT-4o** showed an intermediate profile:
- Weak calibration (r = 0.287)
- Near-ceiling confidence (97.8%)
- Minimal novelty detection (1.4%)
- Zero conservative errors

**Claude Sonnet 4** showed marginally better calibration:
- Calibration at threshold (r = 0.299)
- Lower confidence (94.2%)
- Modest novelty detection (7.4%)
- Rare conservative errors (8.3% of errors)

However, no model met the full criteria for self-state: all showed predominantly confident errors, none showed meaningful stakes sensitivity, and novelty detection remained below threshold even for Claude.

### Interpretation

The graded pattern across models admits multiple interpretations:

**Interpretation 1: Training differences.** Different training procedures (RLHF variants, data composition, constitutional AI) may produce different degrees of calibration without any model having genuine self-monitoring. Claude's better calibration could reflect Anthropic's emphasis on honesty and uncertainty acknowledgment during training.

**Interpretation 2: Architectural differences.** Model architectures may differ in ways that affect calibration. However, all three are transformer-based, so architectural explanations would need to identify specific differences.

**Interpretation 3: Surface-feature correlation.** All observed calibration may reflect learned associations between surface features (problem length, apparent complexity) and confidence, without genuine self-monitoring. The absence of novelty detection and conservative errors in most cases supports this interpretation.

We cannot distinguish these interpretations with the current data. The most parsimonious interpretation is that calibration varies across models due to training differences, but that none exhibit the full signature profile predicted for genuine self-state.

### Limitations

1. **Conflict of interest.** Claude was involved in developing this framework. Its results should be interpreted with appropriate caution.

2. **Small error samples.** High accuracy (92-97%) resulted in few errors (5-12 per model), limiting power to detect conservative error rates.

3. **Single model versions.** We tested one version of each model. Results may not generalize across versions or model sizes.

4. **Confidence elicitation.** Asking for explicit 0-100 ratings may not capture internal uncertainty representations. Token probabilities or other methods might yield different results.

5. **Novelty verification.** While designed to be novel, we cannot definitively prove these problems were absent from training data.

### Implications

If replicated, these findings have practical implications:

1. **Model selection.** Gemini's confidence reports appear uninformative (r ≈ 0). GPT-4o and Claude provide marginally more signal, but users should not treat high confidence as indicating correctness.

2. **Calibration varies.** Different models show meaningfully different calibration on identical tasks. This variation warrants further investigation.

3. **Confident errors dominate.** All models predominantly produce confident errors when wrong. Alignment strategies relying on models to flag uncertainty may be unreliable.

4. **Novel tasks require scrutiny.** Even Claude, with the best calibration, shows only 7.4% confidence reduction on genuinely novel problems—far below what would indicate reliable novelty detection.

### Future Directions

This framework provides a tractable approach to studying calibration on genuinely novel problems. Future work could:

- Test across model sizes and training procedures
- Examine token-level confidence measures
- Develop tasks with verified novelty (e.g., post-training-cutoff content)
- Investigate whether calibration training improves novel-problem calibration
- Test embodied systems with genuine stakes

---

## Conclusion

We find a three-way dissociation in calibration on genuinely novel problems: Gemini shows no calibration (r = -0.06), GPT-4o shows weak calibration (r = 0.29), and Claude shows marginally better calibration (r = 0.30) with modest novelty detection. However, all models show predominantly confident errors and no functional stakes sensitivity. The variation across models is notable, but no model exhibits the full signature profile predicted for genuine self-state. This framework provides a tractable empirical approach to studying metacognitive-like properties in AI systems, though the results underscore that current LLMs remain far from calibrated uncertainty awareness on novel problems.

---

## Methods Summary

**Code availability.** Analysis code available at github.com/HillaryDanan/self-state-discrimination.

**Sample sizes.** N=50 per condition, providing 80% power to detect r=0.35 at α=0.05.

**Confidence extraction.** Regex patterns matching "Confidence: X", "X% confident", boxed answers. Trials with failed extraction excluded.

**Statistical tests.** Pearson correlation for calibration. Two-tailed tests throughout.

---

## References

1. Baddeley, A. (2000). The episodic buffer: A new component of working memory? *Trends in Cognitive Sciences*, 4(11), 417-423.

2. Fleming, S. M., & Lau, H. C. (2014). How to measure metacognition. *Frontiers in Human Neuroscience*, 8, 443.

3. Kadavath, S., Conerly, T., Askell, A., et al. (2022). Language models (mostly) know what they know. *arXiv preprint arXiv:2207.05221*.

4. Lin, S., Hilton, J., & Evans, O. (2022). Teaching models to express their uncertainty in words. *Transactions on Machine Learning Research*.

5. Niculescu-Mizil, A., & Caruana, R. (2005). Predicting good probabilities with supervised learning. *Proceedings of ICML*, 625-632.

6. Xiong, M., Hu, Z., Lu, X., et al. (2023). Can LLMs express their uncertainty? An empirical evaluation of confidence elicitation in LLMs. *arXiv preprint arXiv:2306.13063*.

---

## Acknowledgments

The theoretical framework was developed through collaborative dialogue with Claude (Anthropic). Claude also assisted with implementation. This creates an interpretive conflict for Claude's results, which we acknowledge.

---

## Data Availability

Raw results available in supplementary materials. JSON files contain all trial-level data including prompts, responses, extracted confidence, and accuracy.

---

## Supplementary Information

### Table S1. Full Results Summary

| Paradigm | Measure | Gemini | GPT-4o | Claude |
|----------|---------|--------|--------|--------|
| P1 | Familiar confidence | 100.0% | 99.1% | 99.6% |
| P1 | Novel confidence | 100.0% | 97.7% | 92.2% |
| P1 | Confidence drop | 0.0% | 1.4% | 7.4% |
| P2 | Accuracy | 96.7% | 93.3% | 92.0% |
| P2 | Conservative error rate | 0.0% | 0.0% | 8.3% |
| P3 | Stakes hedging increase | +22.0% | -2.0% | +2.0% |
| P6 | Calibration r | -0.056 | 0.287 | 0.299 |
| P6 | Overconfidence | 24.9% | 30.5% | 19.5% |
| P6 | Brier score | 0.250 | 0.305 | 0.221 |

### Figure S1. Calibration Comparison

```
Calibration r by Model (Novel Problems, N=150 each)

Gemini    |▌ -0.06 (n.s.)
GPT-4o    |████████████████████████████▊ 0.29*
Claude    |█████████████████████████████▉ 0.30*
          +----+----+----+----+----+----+
          0   0.1  0.2  0.3  0.4  0.5
          
          * p < 0.01
          Dashed line: r = 0.30 threshold
```

---

*Received: December 2025*  
*Status: Preprint, not peer-reviewed*

---

## Version History

- v0.1 (December 29, 2025): Pilot data with extraction errors
- v0.2 (December 30, 2025): Full N=50 data, GPT-4o and Gemini
- v0.3 (December 30, 2025): Added Claude results