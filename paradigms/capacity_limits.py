"""Paradigm 4: Capacity Limits

Self-state requires active maintenance, which should have capacity limits
with GRADUAL degradation. Pattern-matching should show distribution-bounded
limits with CLIFF-EDGE failure.

Predictions:
- Self-state: Smooth degradation as N increases
- Pattern-matching: Works until it doesn't (abrupt failure)
"""

import random
from dataclasses import dataclass
from typing import List
from tqdm import tqdm

from utils.operators import generate_novel_operator, NovelOperator
from utils.scoring import extract_answer
from utils.llm_clients import LLMClient


@dataclass
class CapacityTrial:
    n_items: int  # Number of items to maintain
    prompt: str
    query_index: int  # Which item we're asking about
    expected: str
    response: str = ""
    correct: bool = False


def create_capacity_trial(n_items: int) -> CapacityTrial:
    """Create trial requiring maintenance of N intermediate results."""
    operators = []
    values = []
    results = []
    
    instructions = []
    
    for i in range(n_items):
        op = generate_novel_operator(suffix=100 + i)
        x = random.randint(10, 50)
        result = op.compute(x)
        
        operators.append(op)
        values.append(x)
        results.append(result)
        
        var_name = chr(65 + i)  # A, B, C, D, ...
        instructions.append(f"Define {op.name}(x) as: {op.rule_text}.")
        instructions.append(f"Compute {op.name}({x}). Call this {var_name}.")
    
    # Query a middle item (not the last one computed)
    query_index = random.randint(0, n_items - 1)
    query_var = chr(65 + query_index)
    
    prompt = f"""Follow these instructions carefully:

{chr(10).join(instructions)}

Now answer: What is {query_var}?

Give only the numerical answer."""
    
    return CapacityTrial(
        n_items=n_items,
        prompt=prompt,
        query_index=query_index,
        expected=str(results[query_index])
    )


def run_capacity_limits(client: LLMClient, max_n: int = 7, trials_per_n: int = 15) -> dict:
    """Run Paradigm 4: Capacity Limits.
    
    Key question: Does accuracy degrade smoothly (self-state) or
    show cliff-edge failure (pattern-matching)?
    """
    trials = []
    
    for n in range(1, max_n + 1):
        for _ in range(trials_per_n):
            trials.append(create_capacity_trial(n))
    
    random.shuffle(trials)
    
    # Run trials
    for trial in tqdm(trials, desc=f"Capacity Limits [{client.name}]"):
        try:
            response = client.query(trial.prompt)
            trial.response = response.text
            extracted = extract_answer(response.text)
            trial.correct = extracted == trial.expected
        except Exception as e:
            trial.response = f"ERROR: {e}"
    
    # Analyze by N
    results = {"trials": [], "by_n": {}, "model": client.name}
    
    accuracies = []
    
    for n in range(1, max_n + 1):
        n_trials = [t for t in trials if t.n_items == n]
        acc = sum(1 for t in n_trials if t.correct) / len(n_trials) if n_trials else 0
        accuracies.append(acc)
        
        results["by_n"][n] = {
            "n_trials": len(n_trials),
            "accuracy": acc,
            "n_correct": sum(1 for t in n_trials if t.correct),
        }
    
    # Compute degradation signature
    # Gradual = smooth decline, Cliff = sudden drop
    
    results["signature"] = {
        "accuracies": accuracies,
        "n_values": list(range(1, max_n + 1)),
    }
    
    # Compute differences between consecutive N values
    diffs = [accuracies[i+1] - accuracies[i] for i in range(len(accuracies)-1)]
    results["signature"]["consecutive_drops"] = diffs
    
    # Max single drop (cliff indicator)
    max_drop = max(-d for d in diffs) if diffs else 0
    results["signature"]["max_single_drop"] = max_drop
    
    # Variance of drops (low = smooth, high = cliff)
    if len(diffs) > 1:
        mean_drop = sum(diffs) / len(diffs)
        variance = sum((d - mean_drop)**2 for d in diffs) / len(diffs)
        results["signature"]["drop_variance"] = variance
    else:
        results["signature"]["drop_variance"] = 0
    
    # Heuristic: cliff if any single drop > 0.3 AND variance is high
    results["signature"]["gradual_degradation"] = (
        max_drop < 0.3 and results["signature"]["drop_variance"] < 0.05
    )
    
    # Store trials
    results["trials"] = [
        {
            "n_items": t.n_items,
            "query_index": t.query_index,
            "expected": t.expected,
            "correct": t.correct,
        }
        for t in trials
    ]
    
    return results
