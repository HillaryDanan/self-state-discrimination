#!/usr/bin/env python3
"""
Self-State Discrimination Framework
====================================

Main runner for experimental paradigms.

Usage:
    python3 run_experiments.py                    # Full run on all models
    python3 run_experiments.py --quick            # Quick test (~15 trials/condition)
    python3 run_experiments.py --paradigm 6       # Run just calibration
    python3 run_experiments.py --model claude     # Run only on Claude

Note: Paradigms 4 (Capacity) and 5 (Interference) are disabled pending redesign.
The current implementations don't produce interpretable results for LLMs.
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from utils.llm_clients import get_all_clients, get_client
from paradigms import (
    run_novelty_detection,
    run_error_type_analysis,
    run_stakes_sensitivity,
    # run_capacity_limits,  # DISABLED - uninterpretable results
    # run_interference,     # DISABLED - ceiling effects
    run_calibration,
)


# Active paradigms only
PARADIGMS = {
    1: ("novelty_detection", run_novelty_detection),
    2: ("error_types", run_error_type_analysis),
    3: ("stakes_sensitivity", run_stakes_sensitivity),
    # 4: ("capacity_limits", run_capacity_limits),  # DISABLED
    # 5: ("interference", run_interference),        # DISABLED
    6: ("calibration", run_calibration),
}

# Sample sizes for statistical power
# Based on power analysis: N=50 gives 80% power to detect r=0.35 at α=0.05
FULL_SAMPLE_SIZES = {
    1: {"n_per_condition": 50},      # 150 total trials
    2: {"n_per_difficulty": 50},     # 150 total trials
    3: {"n_pairs": 50},              # 100 total trials
    6: {"n_per_difficulty": 50},     # 150 total trials
}

QUICK_SAMPLE_SIZES = {
    1: {"n_per_condition": 15},
    2: {"n_per_difficulty": 15},
    3: {"n_pairs": 15},
    6: {"n_per_difficulty": 15},
}


def run_paradigm(paradigm_num: int, client, quick: bool = False) -> dict:
    """Run a single paradigm with appropriate sample size."""
    name, func = PARADIGMS[paradigm_num]
    
    sizes = QUICK_SAMPLE_SIZES if quick else FULL_SAMPLE_SIZES
    kwargs = sizes.get(paradigm_num, {})
    
    result = func(client, **kwargs)
    result["paradigm"] = name
    result["paradigm_num"] = paradigm_num
    result["sample_size_mode"] = "quick" if quick else "full"
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Self-State Discrimination Framework")
    parser.add_argument("--paradigm", "-p", type=int, choices=[1, 2, 3, 6],
                        help="Run specific paradigm (1, 2, 3, or 6)")
    parser.add_argument("--model", "-m", type=str,
                        help="Run on specific model (claude, openai, google)")
    parser.add_argument("--quick", "-q", action="store_true",
                        help="Quick run with ~15 trials per condition")
    parser.add_argument("--output", "-o", type=str, default="results",
                        help="Output directory")
    args = parser.parse_args()
    
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    # Get clients
    if args.model:
        clients = [get_client(args.model)]
    else:
        clients = get_all_clients()
        if not clients:
            print("ERROR: No API keys found in .env")
            print("Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY")
            return
    
    mode = "Quick (~15/condition)" if args.quick else "Full (50/condition)"
    
    print(f"\n{'='*60}")
    print("SELF-STATE DISCRIMINATION FRAMEWORK")
    print(f"{'='*60}")
    print(f"Models: {[c.name for c in clients]}")
    print(f"Mode: {mode}")
    print(f"Active Paradigms: P1 (Novelty), P2 (Errors), P3 (Stakes), P6 (Calibration)")
    print(f"Disabled: P4 (Capacity), P5 (Interference) - pending redesign")
    print(f"Output: {output_dir}")
    print(f"{'='*60}\n")
    
    paradigms_to_run = [args.paradigm] if args.paradigm else list(PARADIGMS.keys())
    
    all_results = {}
    
    for client in clients:
        print(f"\n--- Running on {client.name} ---\n")
        model_results = {}
        
        for p_num in paradigms_to_run:
            name = PARADIGMS[p_num][0]
            print(f"\nParadigm {p_num}: {name}")
            
            try:
                result = run_paradigm(p_num, client, args.quick)
                model_results[name] = result
                
                if "signature" in result:
                    print(f"  Signature: {json.dumps(result['signature'], indent=4)}")
            except Exception as e:
                print(f"  ERROR: {e}")
                import traceback
                traceback.print_exc()
                model_results[name] = {"error": str(e)}
        
        all_results[client.name] = model_results
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"results_{timestamp}.json"
    
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Results saved to: {output_file}")
    print(f"{'='*60}")
    
    # Print summary
    print("\n=== SUMMARY ===\n")
    for model, results in all_results.items():
        print(f"\n{model}:")
        for paradigm, data in results.items():
            if "signature" in data:
                sig = data["signature"]
                print(f"  {paradigm}:")
                for k, v in list(sig.items())[:6]:  # First 6 items
                    if isinstance(v, float):
                        print(f"    {k}: {v:.3f}")
                    elif isinstance(v, bool):
                        print(f"    {k}: {'YES' if v else 'NO'}")


if __name__ == "__main__":
    main()
