
import streamlit as st
import pandas as pd
from src.config import GRIS


def _as_bool(serie: pd.Series) -> pd.Series:
    return serie.astype(str).str.lower().isin(["true", "1"])


def _subtitulo(texto_html: str) -> None:
    st.markdown(
        f"<p style='font-size:1.05rem; font-weight:600; margin-bottom:0.4rem'>{texto_html}</p>",
        unsafe_allow_html=True,
    )


def _kpi(
    col,
    label: str,
    value: str,
    color: str = "inherit",
) -> None:
    col.markdown(
        f"<div style='line-height:1.15'>"
        f"<div style='font-size:0.8rem; color:{GRIS}'>{label}</div>"
        f"<div style='font-size:2.1rem; font-weight:700; color:{color}'>{value}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
