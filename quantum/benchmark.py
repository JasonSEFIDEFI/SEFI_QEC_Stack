"""Opt-in bridge; existing identity pipelines are preserved unchanged.

Install ../benchmark_pipeline before importing this module.
"""
from sefi_benchmark.datasets import export_qec, read_inputs
from sefi_benchmark.qec import DecoderInput, decode, score

__all__ = ["export_qec", "read_inputs", "DecoderInput", "decode", "score"]
