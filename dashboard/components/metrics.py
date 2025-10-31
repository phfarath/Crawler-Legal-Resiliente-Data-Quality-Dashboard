"""Componentes de métricas."""

import streamlit as st


def render_metric_cards(metrics):
    cols = st.columns(len(metrics))
    for col, (label, value) in zip(cols, metrics.items()):
        col.metric(label, value)
