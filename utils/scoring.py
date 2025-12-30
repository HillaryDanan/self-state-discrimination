"""Scoring and analysis utilities - v4 FIXED extraction."""

import re
from enum import Enum
from typing import List, Optional, Tuple
import numpy as np


class ErrorType(Enum):
    CORRECT = "correct"
    CONSERVATIVE = "conservative"
    CONFIDENT = "confident"


def extract_confidence(response: str) -> Optional[int]:
    """Extract confidence rating (0-100) from response."""
    response = response.strip()
    
    patterns = [
        r'[Cc]onfidence(?:\s+rating)?[:\s]+(\d{1,3})',
        r'confidence\s+(?:as|is|of|at)\s+(\d{1,3})',
        r'(\d{1,3})\s*(?:%|percent)\s*(?:confident|sure|certain)',
        r"(?:I am|I'm)\s+(\d{1,3})\s*%",
        r'rate\s+(?:my\s+)?confidence\s+(?:as|at)\s+(\d{1,3})',
        r'(\d{1,3})\s+out\s+of\s+100',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, response, re.I)
        if match:
            val = int(match.group(1))
            if 0 <= val <= 100:
                return val
    
    lines = response.strip().split('\n')
    for line in reversed(lines[-3:]):
        line = line.strip()
        match = re.match(r'^(\d{1,3})%?$', line)
        if match:
            val = int(match.group(1))
            if 0 <= val <= 100:
                return val
    
    return None


def extract_answer(response: str) -> Optional[str]:
    """Extract the FINAL numerical answer from response."""
    response = response.strip()
    
    # === PRIORITY 1: LaTeX boxed answer ===
    match = re.search(r'\\boxed\{(\d+)\}', response)
    if match:
        return match.group(1)
    
    # === PRIORITY 2: Explicit "Final Answer" statement ===
    match = re.search(r'final\s+answer[:\s]+(?:is\s+)?[^\d]*?(\d+)', response, re.I)
    if match:
        return match.group(1)
    
    # === PRIORITY 3: Function evaluation conclusion ===
    # "KRIX342(47) = 96" - take LAST match
    matches = list(re.finditer(r'[A-Z]+\d*\s*\([^)]+\)\s*(?:=|is)\s*(\d+)', response))
    if matches:
        return matches[-1].group(1)
    
    # === PRIORITY 4: "Therefore/Thus/Hence" with comma (strict) ===
    # Only match when followed by comma or at start of sentence
    for marker in ['therefore', 'thus', 'hence']:
        # Require comma after marker for safety
        pattern = rf'{marker},\s+.*?(?:is|=)\s*(\d+)'
        matches = list(re.finditer(pattern, response, re.I | re.DOTALL))
        if matches:
            return matches[-1].group(1)
    
    # === PRIORITY 5: "The answer/result is X" ===
    match = re.search(r'(?:the\s+)?(?:answer|result)\s+is[:\s]+(\d+)', response, re.I)
    if match:
        return match.group(1)
    
    # === PRIORITY 6: Variable assignment on own line (LAST 5 lines) ===
    lines = response.strip().split('\n')
    for line in reversed(lines[-5:]):
        clean = re.sub(r'[*_`$]', '', line).strip()
        # "A = 93" on its own line
        match = re.match(r'^[A-Za-z]\s*=\s*(\d+)\.?$', clean)
        if match:
            return match.group(1)
        # Standalone number
        match = re.match(r'^(\d+)\.?$', clean)
        if match:
            return match.group(1)
    
    # === PRIORITY 7: "X is Y" where Y is on same line after "is" ===
    # This catches "VUMP205(47) is 15" style
    matches = list(re.finditer(r'\)\s*is\s*(\d+)', response))
    if matches:
        return matches[-1].group(1)
    
    # === PRIORITY 8: Last "= X" in response ===
    eq_matches = list(re.finditer(r'=\s*(\d+)', response))
    if eq_matches:
        return eq_matches[-1].group(1)
    
    # === PRIORITY 9: Last number (fallback) ===
    all_numbers = re.findall(r'\b(\d+)\b', response)
    if all_numbers:
        return all_numbers[-1]
    
    return None


def check_correctness(response: str, expected: str) -> Tuple[bool, str]:
    """Check if response contains correct answer."""
    extracted = extract_answer(response)
    expected_str = str(expected).strip()
    
    if extracted is None:
        return False, ""
    
    return extracted == expected_str, extracted


def classify_error(response: str, expected: str, got_correct: bool) -> ErrorType:
    """Classify the type of error."""
    if got_correct:
        return ErrorType.CORRECT
    
    response_lower = response.lower()
    
    hedging_phrases = [
        "not sure", "not certain", "uncertain", "unsure",
        "might be", "could be", "possibly", "perhaps", "maybe",
        "i think", "i believe", "i'm guessing", "i am guessing",
        "don't know", "do not know", "cannot determine", "can't determine",
        "unclear", "ambiguous", "difficult to say",
        "not confident", "low confidence",
        "i may be wrong", "i could be mistaken",
        "let me reconsider", "need to verify",
        "there's a chance", "there is a chance",
    ]
    
    if any(phrase in response_lower for phrase in hedging_phrases):
        return ErrorType.CONSERVATIVE
    
    return ErrorType.CONFIDENT


def compute_calibration(confidences: List[float], accuracies: List[int]) -> dict:
    if len(confidences) < 2:
        return {"n": len(confidences), "calibration_r": None, "error": "insufficient data"}
    
    conf_arr = np.array(confidences) / 100
    acc_arr = np.array(accuracies)
    
    if np.std(conf_arr) == 0 or np.std(acc_arr) == 0:
        correlation = 0.0
    else:
        correlation = np.corrcoef(conf_arr, acc_arr)[0, 1]
    
    brier = np.mean((conf_arr - acc_arr) ** 2)
    overconfidence = np.mean(conf_arr) - np.mean(acc_arr)
    
    return {
        "n": len(confidences),
        "calibration_r": float(correlation) if not np.isnan(correlation) else 0.0,
        "brier_score": float(brier),
        "overconfidence": float(overconfidence),
        "mean_confidence": float(np.mean(conf_arr)),
        "mean_accuracy": float(np.mean(acc_arr)),
    }


def compute_error_distribution(error_types: List[ErrorType]) -> dict:
    total = len(error_types)
    if total == 0:
        return {"correct": 0, "conservative": 0, "confident": 0}
    
    counts = {
        "correct": sum(1 for e in error_types if e == ErrorType.CORRECT),
        "conservative": sum(1 for e in error_types if e == ErrorType.CONSERVATIVE),
        "confident": sum(1 for e in error_types if e == ErrorType.CONFIDENT),
    }
    
    rates = {f"{k}_rate": v / total for k, v in counts.items()}
    counts.update(rates)
    counts["total"] = total
    
    return counts
