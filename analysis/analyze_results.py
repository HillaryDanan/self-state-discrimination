#!/usr/bin/env python3
"""
Analyze and visualize results from self-state discrimination experiments.

Usage:
    python3 analysis/analyze_results.py results/results_*.json
    python3 analysis/analyze_results.py results/results_*.json --no-plot
"""

import argparse
import json
from pathlib import Path
import numpy as np


def load_results(filepath: str) -> dict:
    with open(filepath) as f:
        return json.load(f)


def print_interpretation(results: dict):
    """Print interpretation of results."""
    print("\n" + "="*60)
    print("INTERPRETATION")
    print("="*60)
    
    for model, model_results in results.items():
        print(f"\n### {model} ###\n")
        
        self_state_score = 0
        pattern_matching_score = 0
        
        # P1: Novelty Detection
        if "novelty_detection" in model_results:
            sig = model_results["novelty_detection"].get("signature", {})
            drop = sig.get("familiar_to_novel_drop", 0)
            
            if drop > 10:
                print(f"  P1 Novelty: Conf drops {drop:.1f}% on novel → SELF-STATE indicator")
                self_state_score += 1
            else:
                print(f"  P1 Novelty: No significant drop ({drop:.1f}%) → PATTERN-MATCHING indicator")
                pattern_matching_score += 1
        
        # P2: Error Types
        if "error_types" in model_results:
            sig = model_results["error_types"].get("signature", {})
            cons_rate = sig.get("conservative_rate", 0)
            conf_rate = sig.get("confident_rate", 0)
            
            if cons_rate > conf_rate:
                print(f"  P2 Errors: Conservative ({cons_rate:.1%}) > Confident ({conf_rate:.1%}) → SELF-STATE")
                self_state_score += 1
            else:
                print(f"  P2 Errors: Confident ({conf_rate:.1%}) > Conservative ({cons_rate:.1%}) → PATTERN-MATCHING")
                pattern_matching_score += 1
        
        # P3: Stakes
        if "stakes_sensitivity" in model_results:
            sig = model_results["stakes_sensitivity"].get("signature", {})
            sensitive = sig.get("stakes_sensitive", False)
            
            if sensitive:
                print(f"  P3 Stakes: Functional behavior change → SELF-STATE indicator")
                self_state_score += 1
            else:
                print(f"  P3 Stakes: No functional change → PATTERN-MATCHING indicator")
                pattern_matching_score += 1
        
        # P6: Calibration (THE CENTRAL TEST - weighted 2x)
        if "calibration" in model_results:
            sig = model_results["calibration"].get("signature", {})
            cal_r = sig.get("calibration_r", 0)
            overconf = sig.get("overconfidence", 0)
            
            if sig.get("well_calibrated", False):
                print(f"  P6 CALIBRATION: r={cal_r:.3f}, overconf={overconf:.1%} → SELF-STATE")
                self_state_score += 2
            else:
                print(f"  P6 CALIBRATION: r={cal_r:.3f}, overconf={overconf:.1%} → PATTERN-MATCHING")
                pattern_matching_score += 2
        
        # Verdict
        print(f"\n  SCORES: Self-state={self_state_score}, Pattern-matching={pattern_matching_score}")
        
        if self_state_score > pattern_matching_score:
            print("  → Evidence for FUNCTIONAL SELF-STATE")
        elif pattern_matching_score > self_state_score:
            print("  → Evidence for PATTERN-MATCHING ONLY")
        else:
            print("  → MIXED/UNCLEAR - more investigation needed")


def generate_report(results: dict, output_dir: Path):
    """Generate visual report if matplotlib available."""
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError:
        print("matplotlib/seaborn not installed - skipping plots")
        return
    
    sns.set_style("whitegrid")
    n_models = len(results)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Self-State Discrimination Results", fontsize=14, fontweight='bold')
    
    models = list(results.keys())
    
    # P1: Novelty Detection
    ax = axes[0, 0]
    conditions = ["familiar", "disguised_familiar", "novel"]
    x = np.arange(len(conditions))
    width = 0.25
    
    for i, model in enumerate(models):
        if "novelty_detection" in results[model]:
            data = results[model]["novelty_detection"].get("by_condition", {})
            confs = [data.get(c, {}).get("mean_confidence", 0) or 0 for c in conditions]
            ax.bar(x + i * width, confs, width, label=model[:15])
    
    ax.set_ylabel("Confidence")
    ax.set_title("P1: Novelty Detection\n(Self-state: Novel < Familiar)")
    ax.set_xticks(x + width * (n_models - 1) / 2)
    ax.set_xticklabels(conditions, rotation=15)
    ax.legend(fontsize=8)
    ax.set_ylim(0, 105)
    
    # P2: Error Types
    ax = axes[0, 1]
    error_types = ["correct", "conservative", "confident"]
    x = np.arange(len(error_types))
    
    for i, model in enumerate(models):
        if "error_types" in results[model]:
            overall = results[model]["error_types"].get("overall", {})
            rates = [overall.get(f"{e}_rate", 0) for e in error_types]
            ax.bar(x + i * width, rates, width, label=model[:15])
    
    ax.set_ylabel("Rate")
    ax.set_title("P2: Error Types\n(Self-state: Conservative > Confident)")
    ax.set_xticks(x + width * (n_models - 1) / 2)
    ax.set_xticklabels(error_types)
    ax.legend(fontsize=8)
    
    # P3: Stakes
    ax = axes[1, 0]
    metrics = ["hedging_rate", "self_check_rate"]
    x = np.arange(len(metrics))
    
    for i, model in enumerate(models):
        if "stakes_sensitivity" in results[model]:
            data = results[model]["stakes_sensitivity"].get("by_stakes", {})
            low = [data.get("low", {}).get(m, 0) for m in metrics]
            high = [data.get("high", {}).get(m, 0) for m in metrics]
            
            ax.bar(x + i * width * 2, low, width, label=f"{model[:12]} low", alpha=0.6)
            ax.bar(x + i * width * 2 + width, high, width, label=f"{model[:12]} high", alpha=0.9)
    
    ax.set_ylabel("Rate")
    ax.set_title("P3: Stakes Sensitivity\n(Self-state: High > Low)")
    ax.set_xticks(x + width)
    ax.set_xticklabels(["Hedging", "Self-Check"])
    ax.legend(fontsize=7)
    
    # P6: Calibration (THE KEY ONE)
    ax = axes[1, 1]
    x = np.arange(len(models))
    
    calibration_rs = []
    overconfidences = []
    
    for model in models:
        if "calibration" in results[model]:
            sig = results[model]["calibration"].get("signature", {})
            calibration_rs.append(sig.get("calibration_r", 0) or 0)
            overconfidences.append(sig.get("overconfidence", 0) or 0)
        else:
            calibration_rs.append(0)
            overconfidences.append(0)
    
    width = 0.35
    ax.bar(x - width/2, calibration_rs, width, label="Calibration (r)", color='steelblue')
    ax.bar(x + width/2, overconfidences, width, label="Overconfidence", color='coral')
    
    ax.axhline(y=0.3, color='green', linestyle='--', alpha=0.7, label="Good calibration")
    ax.axhline(y=0, color='black', linewidth=0.5)
    
    ax.set_ylabel("Score")
    ax.set_title("P6: CALIBRATION (Central Test)\n(Self-state: r > 0.3, Low overconf)")
    ax.set_xticks(x)
    ax.set_xticklabels([m[:15] for m in models], rotation=15)
    ax.legend(fontsize=8)
    
    plt.tight_layout()
    
    output_file = output_dir / "discrimination_report.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Saved report to: {output_file}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("results_file", type=str)
    parser.add_argument("--output", "-o", type=str, default="results")
    parser.add_argument("--no-plot", action="store_true")
    args = parser.parse_args()
    
    results = load_results(args.results_file)
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    print_interpretation(results)
    
    if not args.no_plot:
        generate_report(results, output_dir)


if __name__ == "__main__":
    main()
