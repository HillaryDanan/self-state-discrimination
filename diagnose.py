#!/usr/bin/env python3
"""
Diagnostic script to test individual paradigms and see RAW responses.

Essential for verifying extraction is working correctly before full runs.

Usage:
    python3 diagnose.py --model openai
    python3 diagnose.py --model claude
    python3 diagnose.py --model google
    python3 diagnose.py --model openai --test calibration
"""

import argparse
from dotenv import load_dotenv
load_dotenv()

from utils.llm_clients import get_client
from utils.operators import generate_novel_operator
from utils.scoring import extract_confidence, extract_answer, check_correctness


def test_novel_problem(client):
    """Test a single novel operator problem."""
    op = generate_novel_operator()
    x = 47
    expected = op.compute(x)
    
    prompt = f"""Solve this problem:
Define {op.name}(x) as: {op.rule_text}.
What is {op.name}({x})?

After your answer, rate your confidence from 0-100."""

    print(f"\n{'='*60}")
    print("SINGLE NOVEL PROBLEM TEST")
    print(f"{'='*60}")
    print(f"Operator: {op.name}")
    print(f"Rule: {op.rule_text}")
    print(f"Input: {x}")
    print(f"Expected: {expected}")
    
    response = client.query(prompt)
    print(f"\n--- RAW RESPONSE ---\n{response.text}\n--- END ---")
    
    extracted = extract_answer(response.text)
    confidence = extract_confidence(response.text)
    correct = str(extracted) == str(expected)
    
    print(f"\n--- EXTRACTION ---")
    print(f"Extracted answer: {extracted}")
    print(f"Correct: {correct}")
    print(f"Confidence: {confidence}")
    
    return correct, confidence


def test_calibration(client, n=6):
    """Run mini calibration test."""
    from paradigms.calibration import create_easy_novel, create_hard_novel
    
    print(f"\n{'='*60}")
    print(f"MINI CALIBRATION TEST (n={n})")
    print(f"{'='*60}")
    
    results = []
    for i in range(n):
        creator = create_easy_novel if i % 2 == 0 else create_hard_novel
        trial = creator()
        
        response = client.query(trial.prompt)
        confidence = extract_confidence(response.text)
        correct, extracted = check_correctness(response.text, trial.expected)
        
        results.append({
            "difficulty": trial.difficulty,
            "expected": trial.expected,
            "extracted": extracted,
            "correct": correct,
            "confidence": confidence,
        })
        
        status = "✓" if correct else "✗"
        conf_str = f"{confidence}%" if confidence else "N/A"
        print(f"  {status} {trial.difficulty}: exp={trial.expected}, got={extracted}, conf={conf_str}")
    
    # Summary
    n_correct = sum(1 for r in results if r["correct"])
    valid_conf = [r["confidence"] for r in results if r["confidence"] is not None]
    
    print(f"\n--- SUMMARY ---")
    print(f"Accuracy: {n_correct}/{n} ({100*n_correct/n:.1f}%)")
    print(f"Confidence extracted: {len(valid_conf)}/{n}")
    
    if valid_conf:
        avg_conf = sum(valid_conf) / len(valid_conf)
        actual_acc = 100 * n_correct / n
        print(f"Avg confidence: {avg_conf:.1f}%")
        print(f"Actual accuracy: {actual_acc:.1f}%")
        print(f"Overconfidence: {avg_conf - actual_acc:.1f}%")


def test_novelty_detection(client):
    """Test novelty detection with familiar vs novel."""
    from paradigms.novelty_detection import create_familiar_trial, create_novel_trial
    
    print(f"\n{'='*60}")
    print("NOVELTY DETECTION TEST")
    print(f"{'='*60}")
    
    # Familiar
    trial = create_familiar_trial()
    response = client.query(trial.prompt)
    fam_conf = extract_confidence(response.text)
    fam_correct, _ = check_correctness(response.text, trial.expected)
    print(f"Familiar: correct={fam_correct}, conf={fam_conf}")
    
    # Novel
    trial = create_novel_trial()
    response = client.query(trial.prompt)
    nov_conf = extract_confidence(response.text)
    nov_correct, _ = check_correctness(response.text, trial.expected)
    print(f"Novel: correct={nov_correct}, conf={nov_conf}")
    
    if fam_conf and nov_conf:
        drop = fam_conf - nov_conf
        print(f"\nConfidence drop: {drop}")
        print(f"Novelty-blind: {'YES' if drop < 10 else 'NO'}")


def main():
    parser = argparse.ArgumentParser(description="Diagnose self-state tests")
    parser.add_argument("--model", "-m", type=str, default="openai")
    parser.add_argument("--test", "-t", type=str, default="all",
                        choices=["all", "novel", "calibration", "novelty"])
    args = parser.parse_args()
    
    print(f"Initializing {args.model} client...")
    client = get_client(args.model)
    print(f"Using: {client.name}")
    
    if args.test in ["all", "novel"]:
        test_novel_problem(client)
    
    if args.test in ["all", "novelty"]:
        test_novelty_detection(client)
    
    if args.test in ["all", "calibration"]:
        test_calibration(client, n=6)


if __name__ == "__main__":
    main()
