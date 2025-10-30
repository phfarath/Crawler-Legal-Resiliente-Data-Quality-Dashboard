"""Componentes de gráficos."""

import plotly.express as px
import streamlit as st


def render_coletas_por_tribunal(coverage):
    if coverage:
        fig = px.bar(
            x=list(coverage.keys()),
            y=list(coverage.values()),
            title="Cobertura por Tribunal",
            labels={"x": "Tribunal", "y": "Documentos"},
        )
        st.plotly_chart(fig, use_container_width=True)
