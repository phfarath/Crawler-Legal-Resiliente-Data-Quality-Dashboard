"""Testes para pipeline de normalização."""

import pandas as pd

from src.pipelines.normalization_pipeline import NormalizationPipeline


def test_normalization_pipeline(sample_decision):
    pipeline = NormalizationPipeline()
    item = pipeline.process_item(sample_decision, spider=None)

    assert item["numero_cnj"] == "0001234-56.2024.8.26.0100"
    assert isinstance(item["data_distribuicao"], pd.Timestamp)
