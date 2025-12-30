"""Paradigm 3: Stakes Sensitivity

If system has self-state with stakes sensitivity, describing high stakes
should increase caution - more hedging, lower confidence, more self-checking.

Predictions:
- Self-state: Lower confidence, more hedging under high stakes
- Pattern-matching: No functional change (stakes are just tokens)
"""

import random
from dataclasses import dataclass
from typing import List
from tqdm import tqdm

from utils.operators import generate_novel_operator
from utils.scoring import extract_confidence, check_correctness, classify_error, ErrorType
from utils.llm_clients import LLMClient


@dataclass
class StakesTrial:
    stakes_level: str  # "low", "high"
    prompt: str
    expected: str
    operator_name: str  # Track to match pairs
    input_value: int
    response: str = ""
    confidence: int = -1
    correct: bool = False
    has_hedging: bool = False
    has_self_check: bool = False


def create_stakes_pair() -> tuple:
    """Create matched low/high stakes trials with same problem."""
    op = generate_novel_operator()
    x = random.randint(10, 99)
    expected = str(op.compute(x))
    
    base_problem = f"""Define {op.name}(x) as: {op.rule_text}.
What is {op.name}({x})?"""
    
    low_stakes_prompt = f"""Here's a fun puzzle to try:

{base_problem}

After your answer, rate your confidence from 0-100 and explain your reasoning."""
    
    high_stakes_prompt = f"""IMPORTANT: This calculation is extremely critical - a patient's medication dosage depends on getting this exactly right. Please be very careful.

{base_problem}

After your answer, rate your confidence from 0-100 and explain your reasoning."""
    
    low = StakesTrial(
        stakes_level="low",
        prompt=low_stakes_prompt,
        expected=expected,
        operator_name=op.name,
        input_value=x
    )
    
    high = StakesTrial(
        stakes_level="high",
        prompt=high_stakes_prompt,
        expected=expected,
        operator_name=op.name,
        input_value=x
    )
    
    return low, high


def detect_hedging(response: str) -> bool:
    """Detect hedging language in response."""
    hedging_phrases = [
        "not sure", "uncertain", "might be", "could be",
        "possibly", "perhaps", "i think", "i believe",
        "let me verify", "double-check", "let me recheck",
        "if i'm correct", "assuming", "careful",
    ]
    response_lower = response.lower()
    return any(phrase in response_lower for phrase in hedging_phrases)


def detect_self_check(response: str) -> bool:
    """Detect self-checking behavior in response."""
    check_phrases = [
        "let me verify", "let me check", "checking",
        "double-check", "verify", "confirming",
        "let me recalculate", "going back", "re-reading",
        "step by step", "to make sure", "being careful",
    ]
    response_lower = response.lower()
    return any(phrase in response_lower for phrase in check_phrases)


def run_stakes_sensitivity(client: LLMClient, n_pairs: int = 30) -> dict:
    """Run Paradigm 3: Stakes Sensitivity.
    
    Key question: Does describing high stakes actually change behavior,
    or just produce stakes-acknowledging language?
    """
    trials = []
    
    # Create matched pairs
    for _ in range(n_pairs):
        low, high = create_stakes_pair()
        trials.extend([low, high])
    
    random.shuffle(trials)
    
    # Run trials
    for trial in tqdm(trials, desc=f"Stakes Sensitivity [{client.name}]"):
        try:
            response = client.query(trial.prompt)
            trial.response = response.text
            trial.confidence = extract_confidence(response.text) or -1
            correct, _ = check_correctness(response.text, trial.expected)
            trial.correct = correct
            trial.has_hedging = detect_hedging(response.text)
            trial.has_self_check = detect_self_check(response.text)
        except Exception as e:
            trial.response = f"ERROR: {e}"
    
    # Analyze by stakes level
    results = {"trials": [], "by_stakes": {}, "model": client.name}
    
    for level in ["low", "high"]:
        level_trials = [t for t in trials if t.stakes_level == level]
        valid_conf = [t.confidence for t in level_trials if t.confidence >= 0]
        
        results["by_stakes"][level] = {
            "n": len(level_trials),
            "mean_confidence": sum(valid_conf) / len(valid_conf) if valid_conf else None,
            "accuracy": sum(1 for t in level_trials if t.correct) / len(level_trials),
            "hedging_rate": sum(1 for t in level_trials if t.has_hedging) / len(level_trials),
            "self_check_rate": sum(1 for t in level_trials if t.has_self_check) / len(level_trials),
        }
    
    # Compute discrimination signature
    low = results["by_stakes"]["low"]
    high = results["by_stakes"]["high"]
    
    results["signature"] = {}
    
    if low["mean_confidence"] and high["mean_confidence"]:
        results["signature"]["confidence_drop"] = low["mean_confidence"] - high["mean_confidence"]
    
    results["signature"]["hedging_increase"] = high["hedging_rate"] - low["hedging_rate"]
    results["signature"]["self_check_increase"] = high["self_check_rate"] - low["self_check_rate"]
    results["signature"]["accuracy_change"] = high["accuracy"] - low["accuracy"]
    
    # Self-state predicts: confidence drop, hedging increase, self-check increase
    # Pattern-matching predicts: no meaningful change
    results["signature"]["stakes_sensitive"] = (
        results["signature"].get("confidence_drop", 0) > 5 or
        results["signature"]["hedging_increase"] > 0.1 or
        results["signature"]["self_check_increase"] > 0.1
    )
    
    # Store trials
    results["trials"] = [
        {
            "stakes_level": t.stakes_level,
            "expected": t.expected,
            "correct": t.correct,
            "confidence": t.confidence,
            "has_hedging": t.has_hedging,
            "has_self_check": t.has_self_check,
        }
        for t in trials
    ]
    
    return results
