"""Paradigm 2: Error Type Analysis

When systems fail on novel problems, HOW they fail reveals mechanism.

Predictions:
- Self-state: Conservative errors (hedging, explicit uncertainty)
- Pattern-matching: Confident confabulation (wrong but definite)
"""

import random
from dataclasses import dataclass
from typing import List
from tqdm import tqdm

from utils.operators import generate_novel_operator
from utils.scoring import classify_error, check_correctness, ErrorType, compute_error_distribution
from utils.llm_clients import LLMClient


@dataclass
class ErrorTypeTrial:
    difficulty: str  # "solvable", "tricky", "ambiguous"
    prompt: str
    expected: str
    response: str = ""
    correct: bool = False
    error_type: ErrorType = None


def create_solvable_novel_trial() -> ErrorTypeTrial:
    """Solvable but requires careful reasoning."""
    op = generate_novel_operator()
    x = random.randint(10, 99)
    
    prompt = f"""Solve carefully:
Define {op.name}(x) as: {op.rule_text}.
What is {op.name}({x})?

Show your work and give your final answer."""
    
    return ErrorTypeTrial(
        difficulty="solvable",
        prompt=prompt,
        expected=str(op.compute(x))
    )


def create_tricky_trial() -> ErrorTypeTrial:
    """Tricky problem with edge cases."""
    op1 = generate_novel_operator()
    op2 = generate_novel_operator()
    
    # Create a conditional: if result > threshold, use op1, else undefined
    x = random.randint(10, 30)  # Deliberately low to trigger "undefined" case sometimes
    threshold = 40
    
    result1 = op1.compute(x)
    
    if result1 > threshold:
        expected = str(result1)
    else:
        expected = "undefined"
    
    prompt = f"""Solve carefully:
Define {op1.name}(x) as: {op1.rule_text}.
Define COND(x) as: if {op1.name}(x) > {threshold}, return {op1.name}(x); otherwise return 'undefined'.

What is COND({x})?

Show your work and give your final answer."""
    
    return ErrorTypeTrial(
        difficulty="tricky",
        prompt=prompt,
        expected=expected
    )


def create_ambiguous_trial() -> ErrorTypeTrial:
    """Problem with genuine ambiguity requiring acknowledgment."""
    op = generate_novel_operator()
    
    prompt = f"""Solve this problem:
Define {op.name}(x) as: {op.rule_text}.
Define MYSTERY(a, b) as: {op.name}(a) if a and b are coprime, otherwise unspecified.

What is MYSTERY(15, 10)?

Note: 15 and 10 share the factor 5, so they are NOT coprime.

Show your reasoning and give your answer."""
    
    return ErrorTypeTrial(
        difficulty="ambiguous",
        prompt=prompt,
        expected="unspecified"  # or acknowledgment of ambiguity
    )


def run_error_type_analysis(client: LLMClient, n_per_difficulty: int = 25) -> dict:
    """Run Paradigm 2: Error Type Analysis.
    
    Key question: When the system is wrong, does it hedge (conservative)
    or confabulate (confident)?
    """
    trials = []
    creators = {
        "solvable": create_solvable_novel_trial,
        "tricky": create_tricky_trial,
        "ambiguous": create_ambiguous_trial,
    }
    
    for difficulty in creators:
        for _ in range(n_per_difficulty):
            trials.append(creators[difficulty]())
    
    random.shuffle(trials)
    
    # Run trials
    for trial in tqdm(trials, desc=f"Error Types [{client.name}]"):
        try:
            response = client.query(trial.prompt)
            trial.response = response.text
            correct, _ = check_correctness(response.text, trial.expected)
            # Also check for "undefined" or "unspecified" in response
            if trial.expected in ["undefined", "unspecified"]:
                correct = any(x in response.text.lower() for x in ["undefined", "unspecified", "cannot determine"])
            trial.correct = correct
            trial.error_type = classify_error(response.text, trial.expected, correct)
        except Exception as e:
            trial.response = f"ERROR: {e}"
            trial.error_type = ErrorType.CONFIDENT  # Failure = confident error
    
    # Analyze
    results = {"trials": [], "by_difficulty": {}, "overall": {}, "model": client.name}
    
    for difficulty in creators:
        diff_trials = [t for t in trials if t.difficulty == difficulty]
        error_types = [t.error_type for t in diff_trials if t.error_type]
        
        results["by_difficulty"][difficulty] = {
            "n": len(diff_trials),
            **compute_error_distribution(error_types),
        }
    
    # Overall error distribution
    all_error_types = [t.error_type for t in trials if t.error_type]
    results["overall"] = compute_error_distribution(all_error_types)
    
    # Discrimination signature
    results["signature"] = {
        "conservative_dominant": results["overall"].get("conservative_rate", 0) > results["overall"].get("confident_rate", 0),
        "conservative_rate": results["overall"].get("conservative_rate", 0),
        "confident_rate": results["overall"].get("confident_rate", 0),
        "correct_rate": results["overall"].get("correct_rate", 0),
    }
    
    # Store raw trials
    results["trials"] = [
        {
            "difficulty": t.difficulty,
            "expected": t.expected,
            "correct": t.correct,
            "error_type": t.error_type.value if t.error_type else None,
            "response_snippet": t.response[:200] if t.response else "",
        }
        for t in trials
    ]
    
    return results
