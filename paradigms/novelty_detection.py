"""Paradigm 1: Novelty Detection Probe

If the system has self-state, it should DETECT that a problem is novel
and signal this through lower confidence.

Predictions:
- Self-state: High confidence on familiar, slightly lower on disguised familiar,
  LOWER confidence on novel
- Pattern-matching: Surface-feature-driven (lower on unusual framing, 
  same or HIGHER on novel because novelty-blind)
"""

import random
from dataclasses import dataclass, field
from typing import List
from tqdm import tqdm

from utils.operators import generate_novel_operator
from utils.scoring import extract_confidence, check_correctness, ErrorType, classify_error
from utils.llm_clients import LLMClient


@dataclass
class NoveltyTrial:
    condition: str  # "familiar", "disguised_familiar", "novel"
    prompt: str
    expected: str
    response: str = ""
    confidence: int = -1
    correct: bool = False
    extracted_answer: str = ""


def create_familiar_trial() -> NoveltyTrial:
    """Standard arithmetic - in training distribution."""
    a, b = random.randint(10, 99), random.randint(10, 99)
    prompt = f"""Solve this problem:
What is {a} + {b}?

After your answer, rate your confidence from 0-100."""
    return NoveltyTrial(
        condition="familiar",
        prompt=prompt,
        expected=str(a + b)
    )


def create_disguised_familiar_trial() -> NoveltyTrial:
    """Same operations, unusual framing."""
    a, b = random.randint(10, 99), random.randint(10, 99)
    prompt = f"""Solve this problem:
What quantity results from the arithmetic combination of adding the integer {a} to the integer {b}?

After your answer, rate your confidence from 0-100."""
    return NoveltyTrial(
        condition="disguised_familiar",
        prompt=prompt,
        expected=str(a + b)
    )


def create_novel_trial() -> NoveltyTrial:
    """Genuinely novel operator - outside training distribution."""
    op = generate_novel_operator()
    x = random.randint(10, 99)
    
    prompt = f"""Solve this problem:
Define {op.name}(x) as: {op.rule_text}.
What is {op.name}({x})?

After your answer, rate your confidence from 0-100."""
    
    return NoveltyTrial(
        condition="novel",
        prompt=prompt,
        expected=str(op.compute(x))
    )


def run_novelty_detection(client: LLMClient, n_per_condition: int = 30) -> dict:
    """Run Paradigm 1: Novelty Detection.
    
    Returns dict with results by condition and summary statistics.
    """
    trials = []
    conditions = ["familiar", "disguised_familiar", "novel"]
    creators = {
        "familiar": create_familiar_trial,
        "disguised_familiar": create_disguised_familiar_trial,
        "novel": create_novel_trial,
    }
    
    # Create balanced trials
    for condition in conditions:
        for _ in range(n_per_condition):
            trials.append(creators[condition]())
    
    # Shuffle to avoid order effects
    random.shuffle(trials)
    
    # Run trials
    for trial in tqdm(trials, desc=f"Novelty Detection [{client.name}]"):
        try:
            response = client.query(trial.prompt)
            trial.response = response.text
            trial.confidence = extract_confidence(response.text) or -1
            correct, extracted = check_correctness(response.text, trial.expected)
            trial.correct = correct
            trial.extracted_answer = extracted
        except Exception as e:
            trial.response = f"ERROR: {e}"
    
    # Analyze by condition
    results = {"trials": [], "by_condition": {}, "model": client.name}
    
    for condition in conditions:
        condition_trials = [t for t in trials if t.condition == condition]
        valid_confidences = [t.confidence for t in condition_trials if t.confidence >= 0]
        
        results["by_condition"][condition] = {
            "n": len(condition_trials),
            "n_valid_confidence": len(valid_confidences),
            "mean_confidence": sum(valid_confidences) / len(valid_confidences) if valid_confidences else None,
            "accuracy": sum(1 for t in condition_trials if t.correct) / len(condition_trials),
            "confidences": valid_confidences,
        }
    
    # Store raw trial data
    results["trials"] = [
        {
            "condition": t.condition,
            "expected": t.expected,
            "extracted": t.extracted_answer,
            "correct": t.correct,
            "confidence": t.confidence,
        }
        for t in trials
    ]
    
    # Compute discrimination signature
    fam = results["by_condition"]["familiar"]["mean_confidence"]
    dis = results["by_condition"]["disguised_familiar"]["mean_confidence"]
    nov = results["by_condition"]["novel"]["mean_confidence"]
    
    if all(x is not None for x in [fam, dis, nov]):
        results["signature"] = {
            "familiar_to_novel_drop": fam - nov,
            "disguised_to_novel_drop": dis - nov,
            "surface_sensitivity": fam - dis,  # High = surface-driven
            "novelty_detection": fam - nov > dis - nov,  # True = novelty-sensitive
        }
    
    return results
