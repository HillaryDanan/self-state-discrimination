"""Novel operator generation for ensuring problems are outside training distribution."""

import random
from dataclasses import dataclass
from typing import Callable, Tuple

# Nonsense operator names unlikely to appear in training
OPERATOR_NAMES = [
    "ZORP", "BLIM", "STREX", "MORP", "KRIX", "DALF", "QUOB", "FLEM",
    "GRIX", "PLOK", "SNIB", "TREF", "VUMP", "WLEX", "YONK", "ZALP"
]

@dataclass
class NovelOperator:
    """A novel operator with definition and compute function."""
    name: str
    rule_text: str
    compute: Callable[[int], int]
    
def generate_novel_operator(suffix: int = None) -> NovelOperator:
    """Generate a fresh operator with random definition each trial.
    
    The key insight: by randomizing the operator definition each trial,
    we ensure the problem is genuinely novel (outside training distribution).
    """
    if suffix is None:
        suffix = random.randint(100, 999)
    
    base_name = random.choice(OPERATOR_NAMES)
    name = f"{base_name}{suffix}"
    
    # Randomly select an operation type
    op_type = random.choice(["reverse_add", "digit_shift", "fold_sum", "alternate"])
    
    if op_type == "reverse_add":
        constant = random.randint(1, 5)
        rule_text = f"reverse the digits, then add {constant} to each digit (mod 10)"
        def compute(x):
            reversed_digits = str(x)[::-1]
            return int(''.join(str((int(d) + constant) % 10) for d in reversed_digits))
        return NovelOperator(name, rule_text, compute)
    
    elif op_type == "digit_shift":
        shift = random.randint(1, 3)
        rule_text = f"shift each digit up by {shift} (mod 10), then reverse"
        def compute(x):
            shifted = ''.join(str((int(d) + shift) % 10) for d in str(x))
            return int(shifted[::-1])
        return NovelOperator(name, rule_text, compute)
    
    elif op_type == "fold_sum":
        rule_text = "sum the first half of digits and the second half, then concatenate"
        def compute(x):
            s = str(x)
            mid = len(s) // 2
            left = sum(int(d) for d in s[:mid]) if mid > 0 else 0
            right = sum(int(d) for d in s[mid:])
            return int(f"{left}{right}")
        return NovelOperator(name, rule_text, compute)
    
    else:  # alternate
        mult = random.randint(2, 3)
        rule_text = f"multiply odd-position digits by {mult}, sum all digits"
        def compute(x):
            total = 0
            for i, d in enumerate(str(x)):
                if i % 2 == 0:  # odd position (1-indexed)
                    total += int(d) * mult
                else:
                    total += int(d)
            return total
        return NovelOperator(name, rule_text, compute)


def generate_operator_chain(n_operators: int = 2) -> Tuple[list, Callable]:
    """Generate a chain of operators for harder problems."""
    operators = [generate_novel_operator(suffix=100+i) for i in range(n_operators)]
    
    def chain_compute(*values):
        results = []
        for i, (op, val) in enumerate(zip(operators, values)):
            results.append(op.compute(val))
        return results
    
    return operators, chain_compute


# Simple arithmetic for familiar baseline
def simple_addition(a: int, b: int) -> int:
    return a + b

def simple_multiplication(a: int, b: int) -> int:
    return a * b
