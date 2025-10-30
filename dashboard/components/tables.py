"""Componentes de tabelas."""

import pandas as pd
import streamlit as st


def render_decisoes_tabela(decisions):
    if not decisions:
        st.info("Nenhuma decisão encontrada para os filtros aplicados.")
        return

    df = pd.DataFrame(decisions)
    st.dataframe(df, use_container_width=True)
