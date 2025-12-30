"""Self-State Discrimination Paradigms

Active paradigms that produce interpretable results:

1. Novelty Detection - Does confidence drop on novel problems?
2. Error Types - Conservative vs confident errors?
3. Stakes Sensitivity - Does described stakes change behavior?
6. Calibration - THE CENTRAL TEST: Confidence-accuracy correlation

DISABLED paradigms (pending redesign):

4. Capacity Limits - Current results show non-monotonic patterns
   that are uninterpretable. Transformers may not have "capacity limits"
   in the human working memory sense.
   
5. Interference - Current version produces ceiling effects (100% accuracy).
   LLMs have perfect context access, so standard interference paradigms
   may not apply.
"""

from .novelty_detection import run_novelty_detection
from .error_types import run_error_type_analysis
from .stakes_sensitivity import run_stakes_sensitivity
from .calibration import run_calibration

# DISABLED - kept for reference but not imported
# from .capacity_limits import run_capacity_limits
# from .interference import run_interference
