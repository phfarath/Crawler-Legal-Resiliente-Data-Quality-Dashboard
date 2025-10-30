"""Aplicação Streamlit para monitoramento do crawler."""

import streamlit as st

from dashboard.components.charts import render_coletas_por_tribunal
from dashboard.components.metrics import render_metric_cards
from dashboard.components.tables import render_decisoes_tabela
from dashboard.utils.data_loader import load_dashboard_data
from src.services.quality_checker import QualityChecker
from src.utils.logger import setup_logging

setup_logging()

st.set_page_config(
    page_title="Crawler Legal Resiliente",
    page_icon="⚖️",
    layout="wide",
)

st.title("Crawler Legal Resiliente")

with st.sidebar:
    st.header("Filtros")
    portal_filter = st.selectbox("Portal", ["Todos", "eSAJ", "PJe", "eProc"])
    tribunal_filter = st.text_input("Tribunal", "")

metrics, decisions, coverage = load_dashboard_data(portal_filter, tribunal_filter)

render_metric_cards(metrics)
render_coletas_por_tribunal(coverage)
render_decisoes_tabela(decisions)

quality = QualityChecker()
with st.expander("Métricas de Qualidade"):
    completeness = quality.calculate_completeness()
    st.json(completeness)
