"""Self-State Discrimination Framework - Utilities"""
from .operators import generate_novel_operator, NovelOperator
from .llm_clients import LLMClient, get_client
from .scoring import extract_confidence, classify_error, compute_calibration
