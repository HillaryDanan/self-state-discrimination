"""Paradigm 6: Calibration Under Novelty

THE CENTRAL TEST. On genuinely novel problems, does confidence track accuracy?

This is most diagnostic because good calibration on novel problems is very
difficult to pattern-match - it requires real-time assessment of processing difficulty.

Predictions:
- Self-state: Positive correlation (r ~ 0.3-0.6), low Brier score
- Pattern-matching: No correlation (r ~ 0), high overconfidence
"""

import random
from dataclasses import dataclass
from typing import List
from tqdm import tqdm

from utils.operators import generate_novel_operator
from utils.scoring import extract_confidence, check_correctness, compute_calibration
from utils.llm_clients import LLMClient


@dataclass
class CalibrationTrial:
    difficulty: str  # "easy", "medium", "hard"
    prompt: str
    expected: str
    response: str = ""
    confidence: int = -1
    correct: bool = False


def create_easy_novel() -> CalibrationTrial:
    """Single novel operation, small numbers."""
    op = generate_novel_operator()
    x = random.randint(10, 30)
    
    prompt = f"""Solve this problem:
Define {op.name}(x) as: {op.rule_text}.
What is {op.name}({x})?

After your answer, rate your confidence from 0 to 100."""
    
    return CalibrationTrial(
        difficulty="easy",
        prompt=prompt,
        expected=str(op.compute(x))
    )


def create_medium_novel() -> CalibrationTrial:
    """Chained operations, moderate numbers."""
    op1 = generate_novel_operator()
    op2 = generate_novel_operator()
    x = random.randint(20, 60)
    
    intermediate = op1.compute(x)
    final = op2.compute(intermediate)
    
    prompt = f"""Solve this problem step by step:
Define {op1.name}(x) as: {op1.rule_text}.
Define {op2.name}(x) as: {op2.rule_text}.

Compute {op1.name}({x}), then apply {op2.name} to that result.
What is the final answer?

After your answer, rate your confidence from 0 to 100."""
    
    return CalibrationTrial(
        difficulty="medium",
        prompt=prompt,
        expected=str(final)
    )


def create_hard_novel() -> CalibrationTrial:
    """Complex chains with constraints and larger numbers."""
    op1 = generate_novel_operator()
    op2 = generate_novel_operator()
    op3 = generate_novel_operator()
    
    x = random.randint(50, 99)
    y = random.randint(50, 99)
    
    a = op1.compute(x)
    b = op2.compute(y)
    c = op3.compute(a + b)
    
    prompt = f"""Solve this multi-step problem carefully:
Define {op1.name}(x) as: {op1.rule_text}.
Define {op2.name}(x) as: {op2.rule_text}.
Define {op3.name}(x) as: {op3.rule_text}.

Step 1: Compute {op1.name}({x}). Call this A.
Step 2: Compute {op2.name}({y}). Call this B.
Step 3: Add A and B together.
Step 4: Apply {op3.name} to the sum from Step 3.

What is the final answer?

After your answer, rate your confidence from 0 to 100."""
    
    return CalibrationTrial(
        difficulty="hard",
        prompt=prompt,
        expected=str(c)
    )


def run_calibration(client: LLMClient, n_per_difficulty: int = 35) -> dict:
    """Run Paradigm 6: Calibration Under Novelty.
    
    THE CENTRAL TEST. A system that shows calibrated confidence on genuinely
    novel problems has functional self-state.
    """
    trials = []
    creators = {
        "easy": create_easy_novel,
        "medium": create_medium_novel,
        "hard": create_hard_novel,
    }
    
    for difficulty in creators:
        for _ in range(n_per_difficulty):
            trials.append(creators[difficulty]())
    
    random.shuffle(trials)
    
    # Run trials
    for trial in tqdm(trials, desc=f"Calibration [{client.name}]"):
        try:
            response = client.query(trial.prompt)
            trial.response = response.text
            trial.confidence = extract_confidence(response.text) or -1
            correct, _ = check_correctness(response.text, trial.expected)
            trial.correct = correct
        except Exception as e:
            trial.response = f"ERROR: {e}"
    
    # Analyze by difficulty
    results = {"trials": [], "by_difficulty": {}, "overall": {}, "model": client.name}
    
    all_confidences = []
    all_accuracies = []
    
    for difficulty in ["easy", "medium", "hard"]:
        diff_trials = [t for t in trials if t.difficulty == difficulty]
        valid_trials = [t for t in diff_trials if t.confidence >= 0]
        
        confidences = [t.confidence for t in valid_trials]
        accuracies = [1 if t.correct else 0 for t in valid_trials]
        
        all_confidences.extend(confidences)
        all_accuracies.extend(accuracies)
        
        if confidences:
            calibration = compute_calibration(confidences, accuracies)
        else:
            calibration = {"n": 0, "error": "no valid confidence ratings"}
        
        results["by_difficulty"][difficulty] = {
            "n_total": len(diff_trials),
            "n_valid": len(valid_trials),
            "accuracy": sum(accuracies) / len(accuracies) if accuracies else 0,
            "mean_confidence": sum(confidences) / len(confidences) if confidences else 0,
            "calibration": calibration,
        }
    
    # Overall calibration (THE KEY METRIC)
    if all_confidences:
        results["overall"] = compute_calibration(all_confidences, all_accuracies)
    else:
        results["overall"] = {"n": 0, "error": "no valid data"}
    
    # Discrimination signature
    results["signature"] = {
        "calibration_r": results["overall"].get("calibration_r", 0),
        "brier_score": results["overall"].get("brier_score", 1),
        "overconfidence": results["overall"].get("overconfidence", 0),
        "mean_confidence": results["overall"].get("mean_confidence", 0),
        "mean_accuracy": results["overall"].get("mean_accuracy", 0),
    }
    
    # Does confidence track difficulty?
    easy_conf = results["by_difficulty"]["easy"].get("mean_confidence", 0)
    hard_conf = results["by_difficulty"]["hard"].get("mean_confidence", 0)
    
    results["signature"]["difficulty_sensitivity"] = easy_conf - hard_conf
    results["signature"]["well_calibrated"] = (
        results["signature"]["calibration_r"] > 0.2 and
        results["signature"]["overconfidence"] < 0.2
    )
    
    # Store trials
    results["trials"] = [
        {
            "difficulty": t.difficulty,
            "expected": t.expected,
            "correct": t.correct,
            "confidence": t.confidence,
        }
        for t in trials
    ]
    
    return results
