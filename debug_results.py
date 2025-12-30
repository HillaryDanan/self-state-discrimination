#!/usr/bin/env python3
"""Debug script to examine raw responses and understand failures."""

import json
import sys

def analyze_results(filepath):
    with open(filepath) as f:
        results = json.load(f)
    
    for model, model_results in results.items():
        print(f"\n{'='*60}")
        print(f"MODEL: {model}")
        print(f"{'='*60}")
        
        # Check P6 calibration trials in detail
        if "calibration" in model_results:
            print("\n--- P6 CALIBRATION DEEP DIVE ---")
            trials = model_results["calibration"].get("trials", [])
            
            # Count by confidence extraction
            no_conf = [t for t in trials if t.get("confidence", -1) < 0]
            has_conf = [t for t in trials if t.get("confidence", -1) >= 0]
            
            print(f"Trials with confidence extracted: {len(has_conf)}/{len(trials)}")
            print(f"Trials missing confidence: {len(no_conf)}")
            
            # Accuracy breakdown
            correct = [t for t in trials if t.get("correct")]
            print(f"Correct: {len(correct)}/{len(trials)} ({100*len(correct)/len(trials):.1f}%)")
            
            # By difficulty
            for diff in ["easy", "medium", "hard"]:
                diff_trials = [t for t in trials if t.get("difficulty") == diff]
                diff_correct = [t for t in diff_trials if t.get("correct")]
                diff_conf = [t.get("confidence", 0) for t in diff_trials if t.get("confidence", -1) >= 0]
                avg_conf = sum(diff_conf)/len(diff_conf) if diff_conf else 0
                print(f"  {diff}: {len(diff_correct)}/{len(diff_trials)} correct, avg conf: {avg_conf:.1f}")
        
        # Check P4 capacity
        if "capacity_limits" in model_results:
            print("\n--- P4 CAPACITY DEEP DIVE ---")
            trials = model_results["capacity_limits"].get("trials", [])
            
            for n in range(1, 6):
                n_trials = [t for t in trials if t.get("n_items") == n]
                n_correct = [t for t in n_trials if t.get("correct")]
                print(f"  N={n}: {len(n_correct)}/{len(n_trials)} correct")
                
                # Show some expected vs actual
                for t in n_trials[:2]:
                    print(f"    Expected: {t.get('expected')}, Got correct: {t.get('correct')}")
        
        # Check novelty detection
        if "novelty_detection" in model_results:
            print("\n--- P1 NOVELTY DETECTION DEEP DIVE ---")
            by_cond = model_results["novelty_detection"].get("by_condition", {})
            for cond, data in by_cond.items():
                print(f"  {cond}:")
                print(f"    n={data.get('n')}, valid_conf={data.get('n_valid_confidence')}")
                print(f"    mean_conf={data.get('mean_confidence')}, accuracy={data.get('accuracy'):.2f}")

# Run on the results file
if len(sys.argv) > 1:
    analyze_results(sys.argv[1])
else:
    print("Usage: python3 debug_results.py results/results_*.json")
