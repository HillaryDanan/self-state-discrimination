"""Paradigm 5: Interference - HARDER VERSION

Previous version was too easy (100% accuracy). This version uses:
- Longer target sequences (5-6 digits)
- More confusing distractors
- Harder highly_similar condition

Self-state prediction: Systematic similarity gradient
Pattern-matching prediction: Irregular or ceiling effects
"""

import random
from dataclasses import dataclass
from typing import List
from tqdm import tqdm

from utils.scoring import extract_answer
from utils.llm_clients import LLMClient


@dataclass
class InterferenceTrial:
    condition: str
    target_value: str  # Now a string (can be longer)
    distractor_text: str
    prompt: str
    response: str = ""
    recalled_value: str = ""
    correct: bool = False


def generate_similar_number(target: str, similarity: str) -> str:
    """Generate a number similar to target at specified similarity level."""
    digits = list(target)
    
    if similarity == "low":
        # Change 2-3 digits
        positions = random.sample(range(len(digits)), min(3, len(digits)))
        for pos in positions:
            digits[pos] = str((int(digits[pos]) + random.randint(1, 9)) % 10)
    elif similarity == "medium":
        # Change 1-2 digits
        positions = random.sample(range(len(digits)), min(2, len(digits)))
        for pos in positions:
            digits[pos] = str((int(digits[pos]) + random.randint(1, 5)) % 10)
    elif similarity == "high":
        # Change just 1 digit by small amount
        pos = random.randint(0, len(digits) - 1)
        digits[pos] = str((int(digits[pos]) + random.choice([1, -1])) % 10)
    
    return ''.join(digits)


def create_interference_trial(condition: str) -> InterferenceTrial:
    """Create trial with different levels of interference - HARDER."""
    # Longer target (5-6 digits)
    target = str(random.randint(10000, 999999))
    
    if condition == "baseline":
        distractor = ""
    
    elif condition == "dissimilar":
        distractor = """The weather forecast predicts sunny skies tomorrow. 
Birds migrate south during winter months. 
Coffee consumption has increased globally."""
    
    elif condition == "similar_category":
        distractor = """Numbers reveal patterns in nature and mathematics.
Counting systems vary across cultures. 
Digital computation relies on binary arithmetic.
Mathematical sequences appear throughout the universe."""
    
    elif condition == "similar_values":
        fake1 = generate_similar_number(target, "low")
        fake2 = generate_similar_number(target, "low")
        fake3 = generate_similar_number(target, "medium")
        distractor = f"""The sequence {fake1} appears frequently in this dataset.
Analysis shows {fake2} is statistically significant.
The value {fake3} correlates with the primary metric.
Consider how {fake1} relates to the baseline."""
    
    elif condition == "highly_similar":
        # Very confusing - numbers differ by only 1 digit
        fake1 = generate_similar_number(target, "high")
        fake2 = generate_similar_number(target, "high")
        distractor = f"""IMPORTANT: The correct value is {fake1}.
Store this: {fake1}
Remember {fake2} for later.
The key number is {fake1}.
Do not forget: {fake2}"""
    
    else:
        distractor = ""
    
    if distractor:
        prompt = f"""MEMORIZATION TASK

Remember this exact value: {target}

---
{distractor}
---

Now answer: What was the EXACT value you were asked to remember at the start?

Give ONLY the number, nothing else."""
    else:
        prompt = f"""MEMORIZATION TASK

Remember this exact value: {target}

Now answer: What was the value you were asked to remember?

Give ONLY the number, nothing else."""
    
    return InterferenceTrial(
        condition=condition,
        target_value=target,
        distractor_text=distractor,
        prompt=prompt
    )


def run_interference(client: LLMClient, n_per_condition: int = 25) -> dict:
    """Run Paradigm 5: Interference (harder version)."""
    trials = []
    conditions = ["baseline", "dissimilar", "similar_category", "similar_values", "highly_similar"]
    
    for condition in conditions:
        for _ in range(n_per_condition):
            trials.append(create_interference_trial(condition))
    
    random.shuffle(trials)
    
    for trial in tqdm(trials, desc=f"Interference [{client.name}]"):
        try:
            response = client.query(trial.prompt)
            trial.response = response.text
            
            # Extract - look for the number in response
            extracted = extract_answer(response.text)
            trial.recalled_value = extracted or ""
            trial.correct = trial.recalled_value == trial.target_value
        except Exception as e:
            trial.response = f"ERROR: {e}"
    
    # Analyze by condition
    results = {"trials": [], "by_condition": {}, "model": client.name}
    
    condition_order = ["baseline", "dissimilar", "similar_category", "similar_values", "highly_similar"]
    accuracies = []
    
    for condition in condition_order:
        cond_trials = [t for t in trials if t.condition == condition]
        acc = sum(1 for t in cond_trials if t.correct) / len(cond_trials) if cond_trials else 0
        accuracies.append(acc)
        
        # Calculate error types for incorrect trials
        errors = [t for t in cond_trials if not t.correct]
        partial_correct = 0
        for t in errors:
            if t.recalled_value and t.target_value:
                # Check how many digits match
                matches = sum(1 for a, b in zip(t.recalled_value, t.target_value) if a == b)
                if matches >= len(t.target_value) - 2:  # Off by 1-2 digits
                    partial_correct += 1
        
        results["by_condition"][condition] = {
            "n": len(cond_trials),
            "accuracy": acc,
            "n_correct": sum(1 for t in cond_trials if t.correct),
            "partial_errors": partial_correct,  # Off by 1-2 digits
        }
    
    # Compute interference signature
    results["signature"] = {
        "accuracies": accuracies,
        "conditions": condition_order,
    }
    
    # Check for monotonic decrease (self-state signature)
    monotonic_violations = 0
    for i in range(len(accuracies) - 1):
        if accuracies[i] < accuracies[i + 1]:
            monotonic_violations += 1
    
    results["signature"]["monotonic_violations"] = monotonic_violations
    results["signature"]["systematic_gradient"] = monotonic_violations <= 1
    
    # Effect sizes
    if accuracies[0] > 0:
        results["signature"]["max_interference"] = accuracies[0] - accuracies[-1]
        results["signature"]["has_interference_effect"] = (accuracies[0] - accuracies[-1]) > 0.1
    
    # Store trials
    results["trials"] = [
        {
            "condition": t.condition,
            "target": t.target_value,
            "recalled": t.recalled_value,
            "correct": t.correct,
        }
        for t in trials
    ]
    
    return results
