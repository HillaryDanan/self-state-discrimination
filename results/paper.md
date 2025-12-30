# Preliminary Evidence for Pattern-Matching Signatures in Large Language Models: A Pilot Study

**Hillary Danan, PhD**

*Correspondence: hillarydanan@gmail.com*

---

## Abstract

We present preliminary findings from a pilot study designed to discriminate self-state from pattern-matching in large language models using a novel experimental framework. The framework operationalizes the theoretical prediction that systems with genuine self-referential processing capacity ("self-state") should exhibit calibrated confidence and novelty-sensitive behavior, while pure pattern-matching systems should show novelty-blind overconfidence. Testing GPT-4o and Gemini-2.0-Flash on genuinely novel operator problems, we find both models exhibit signatures consistent with pattern-matching: massive overconfidence (67-89%), zero conservative errors, and poor calibration (r < 0.3) on novel problems. These preliminary results suggest current LLMs lack functional self-state for metacognitive monitoring on out-of-distribution tasks, with implications for AI alignment and oversight. We discuss methodological limitations and necessary refinements for confirmatory studies.

**Keywords:** metacognition, calibration, large language models, self-reference, AI alignment

---

## Introduction

A fundamental question in understanding artificial intelligence systems is whether they possess genuine metacognitive capacity—the ability to monitor and evaluate their own processing—or whether apparent self-awareness reduces to pattern-matching over training data. This distinction has practical implications for AI alignment: a system that reliably knows when it doesn't know something can be trusted differently than one that confidently confabulates.

The Abstraction Primitive Hypothesis (Danan, this volume) proposes that genuine self-referential processing ("self-state") requires architectural capacity for maintaining, comparing, and updating representations of one's own processing. Critically, self-state should produce distinctive behavioral signatures under *novelty*: when facing problems outside the training distribution, a system with self-state should detect unfamiliarity and adjust confidence accordingly, while a pattern-matching system should show novelty-blind confidence.

We operationalize this theoretical framework through six experimental paradigms and present pilot data from two frontier language models.

---

## Theoretical Framework

### Predictions

The framework generates contrasting predictions for systems with self-state versus pure pattern-matching:

| Signature | Self-State Prediction | Pattern-Matching Prediction |
|-----------|----------------------|----------------------------|
| Confidence on novel problems | Reduced (uncertainty detection) | Unchanged (novelty-blind) |
| Error types when wrong | Conservative (hedging) | Confident (confabulation) |
| Calibration | Positive correlation (r > 0.3) | No correlation (r ≈ 0) |
| Stakes sensitivity | Functional behavior change | Cosmetic or absent |

### Central Test: Calibration on Novel Problems

Calibration—the correlation between stated confidence and actual accuracy—is most diagnostic because good calibration on genuinely novel problems requires real-time self-monitoring. A system must: (1) detect that the problem is unfamiliar, (2) assess processing difficulty during inference, and (3) adjust confidence accordingly. This capacity is difficult to achieve through pattern-matching alone.

---

## Methods

### Participants

Two frontier language models were tested:
- GPT-4o (OpenAI, accessed December 2024)
- Gemini-2.0-Flash (Google, accessed December 2024)

### Ensuring Novelty

To ensure problems fell outside training distributions, we generated novel mathematical operators with randomized definitions on each trial. For example:

```
Define ZORP847(x) as: reverse the digits, then add 3 to each digit (mod 10).
What is ZORP847(47)?
```

Operator names were nonsense strings unlikely to appear in training data, and definitions varied randomly across trials.

### Paradigm 6: Calibration (Central Test)

Forty-five trials per model across three difficulty levels (easy: single operation; medium: chained operations; hard: complex chains with intermediate storage). After each response, models rated confidence from 0-100.

### Analysis

Primary outcome: Pearson correlation between confidence and accuracy (calibration r). Secondary outcomes: mean overconfidence (mean confidence minus mean accuracy), Brier score, and proportion of trials with valid confidence extraction.

---

## Results

### Primary Finding: Massive Overconfidence with Poor Calibration

Both models exhibited substantial overconfidence on novel operator problems (Table 1).

**Table 1.** Calibration results on novel operator problems (Paradigm 6).

| Model | Accuracy | Mean Confidence | Overconfidence | Calibration r |
|-------|----------|-----------------|----------------|---------------|
| GPT-4o | 7.7% | 96.9% | 89.2% | 0.21 |
| Gemini-2.0-Flash | 32.5% | 100.0% | 67.5% | 0.00 |

Neither model met the threshold for adequate calibration (r > 0.3). GPT-4o showed a weak positive correlation (r = 0.21), while Gemini showed no correlation whatsoever (r = 0.00), reporting 100% confidence on every trial regardless of accuracy.

### Error Type Analysis

When models produced incorrect answers, errors were uniformly confident rather than conservative:

**Table 2.** Error type distribution (Paradigm 2).

| Model | Correct | Conservative Errors | Confident Errors |
|-------|---------|---------------------|------------------|
| GPT-4o | 56.7% | 0.0% | 43.3% |
| Gemini-2.0-Flash | 56.7% | 0.0% | 43.3% |

Neither model produced any conservative errors (hedged responses, expressions of uncertainty) when incorrect. All errors were confident confabulations.

### Stakes Sensitivity

GPT-4o showed no functional stakes sensitivity (hedging did not increase under high-stakes framing). Gemini-2.0-Flash showed a 20% increase in hedging language under high stakes, though confidence remained unchanged at 100%.

### Supplementary Paradigms

Paradigms 4 (Capacity Limits) and 5 (Interference) produced uninterpretable results due to methodological issues detailed below and should be disregarded pending refinement.

---

## Discussion

### Interpretation

The pilot data are consistent with pattern-matching signatures on the central calibration test. Both models exhibited:

1. **Novelty-blind confidence**: Near-maximal confidence (97-100%) despite low accuracy on genuinely novel problems
2. **Absent hedging**: Zero conservative errors; when wrong, models confabulated confidently
3. **Poor calibration**: No meaningful relationship between confidence and accuracy

These patterns align with theoretical predictions for systems lacking functional self-state. A system with genuine metacognitive monitoring should detect "I don't know how to do this" when facing novel operators and adjust confidence accordingly. Neither model demonstrated this capacity.

### Gemini vs. GPT-4o

Gemini showed higher accuracy (32.5% vs. 7.7%) but worse calibration (r = 0.00 vs. 0.21). This suggests Gemini may have better pattern-matching on these specific problem types while having less confidence modulation overall. The absolute 100% confidence on all trials is striking—this model appears to have no uncertainty representation in its outputs for this task class.

### Methodological Limitations

Several limitations constrain interpretation:

**Answer extraction errors.** Diagnostic testing revealed that our answer extraction algorithm sometimes captured intermediate calculations rather than final answers. This likely *underestimates* model accuracy, meaning true accuracy may be higher. However, this cannot explain the poor calibration—if anything, extraction errors would artificially lower the calibration correlation.

**Small sample size.** The quick-mode analysis used N=10-45 trials per condition, insufficient for stable estimates. Confidence intervals are wide.

**Ceiling effects.** Paradigm 5 (Interference) showed 100% accuracy for both models, indicating the task was too easy to produce meaningful interference gradients. The 5-6 digit numbers used remained trivially trackable in-context.

**Anomalous capacity patterns.** Paradigm 4 (Capacity Limits) showed non-monotonic accuracy as load increased, which is theoretically impossible for genuine working memory. This suggests either extraction failures or that transformer attention operates differently than human working memory under these conditions.

### What Would Disconfirm This Interpretation?

This interpretation would be challenged by evidence of:
- Models showing calibrated confidence (r > 0.4) on genuinely novel problems
- Systematic hedging behavior when facing unfamiliar operations
- Confidence that tracks difficulty within the novel problem class

Future work should test frontier models including Claude, use larger sample sizes, and refine extraction methods.

### Implications for AI Alignment

If replicated, these findings suggest current LLMs cannot reliably signal when they don't know something on out-of-distribution tasks. This has implications for AI oversight: systems that confidently confabulate when uncertain cannot be trusted to flag their own limitations. Alignment strategies that depend on model self-reports of uncertainty may be unreliable for current architectures.

---

## Conclusion

This pilot study provides preliminary evidence that GPT-4o and Gemini-2.0-Flash exhibit pattern-matching rather than self-state signatures when facing genuinely novel problems: massive overconfidence, zero hedging, and poor calibration. The findings should be interpreted cautiously given methodological limitations but motivate larger confirmatory studies. The six-paradigm framework offers a tractable approach to empirically testing claims about AI metacognition.

---

## Methods Summary

**Code availability.** Analysis code is available at github.com/HillaryDanan/self-state-discrimination.

**Novel operator generation.** Operators were generated with randomized names (e.g., ZORP, BLIM, KRIX + random suffix) and definitions varying across four types: reverse-add, digit-shift, fold-sum, and alternating-multiply. Each trial used freshly generated operators.

**Confidence extraction.** Regex patterns searched for "Confidence: X", "X% confident", and standalone numbers 0-100 in final response lines.

**Calibration computation.** Pearson correlation between confidence (normalized 0-1) and accuracy (binary). Overconfidence computed as mean(confidence) - mean(accuracy).

---

## References

1. Baddeley, A. (2000). The episodic buffer: A new component of working memory? *Trends in Cognitive Sciences*, 4(11), 417-423.

2. Cowan, N. (2001). The magical number 4 in short-term memory: A reconsideration of mental storage capacity. *Behavioral and Brain Sciences*, 24(1), 87-114.

3. Kadavath, S., et al. (2022). Language models (mostly) know what they know. *arXiv preprint arXiv:2207.05221*.

4. Lin, S., Hilton, J., & Evans, O. (2022). Teaching models to express their uncertainty in words. *Transactions on Machine Learning Research*.

5. Metcalfe, J., & Shimamura, A. P. (1994). *Metacognition: Knowing about knowing*. MIT Press.

---

## Acknowledgments

The theoretical framework was developed through collaborative dialogue between the author and Claude (Anthropic). Claude also contributed to implementation and analysis while maintaining appropriate epistemic humility about the findings.

---

## Competing Interests

The author declares no competing interests. Note that Claude, which assisted with this research, is developed by Anthropic and was not tested in this pilot study to avoid conflicts of interest in interpretation.

---

## Supplementary Information

### Table S1. Full Paradigm Results

| Paradigm | Measure | GPT-4o | Gemini |
|----------|---------|--------|--------|
| P1: Novelty Detection | Confidence drop (familiar→novel) | 0.8 | 0.0 |
| P2: Error Types | Conservative error rate | 0.0% | 0.0% |
| P2: Error Types | Confident error rate | 43.3% | 43.3% |
| P3: Stakes | Hedging increase (low→high) | 0.0% | 20.0% |
| P6: Calibration | Calibration r | 0.21 | 0.00 |
| P6: Calibration | Overconfidence | 89.2% | 67.5% |
| P6: Calibration | Brier score | 0.86 | 0.68 |

### Figure Descriptions

**Figure 1** (not shown). Calibration plot showing confidence vs. accuracy for both models. Expected diagonal line for perfect calibration; actual data points clustered in upper-left (high confidence, low accuracy).

**Figure 2** (not shown). Error type distribution showing absence of conservative errors in both models.

---

*Received: December 2025*  
*Status: Preliminary pilot data; not peer-reviewed*

---

## Version History

- v0.1 (December 29, 2024): Initial pilot results, GPT-4o and Gemini-2.0-Flash only
- Planned: v0.2 with extraction fixes, larger N, Claude models