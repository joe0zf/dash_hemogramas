import streamlit as st
import pandas as pd

from src.config import ACENTO, GRIS
from src.utils import _as_bool, _kpi, _subtitulo

FLAGS_RELEVANTES = [
    "f_microcitosis", "f_macrocitosis", "f_mchc_baja", "f_eritrocitosis",
    "f_leucopenia", "f_leucocitosis", "f_linfopenia", "f_linfocitosis",
    "f_neu_alto", "f_neu_bajo", "f_trombocitopenia", "f_trombocitosis",
]

def render(df) -> None:
    if df is None or len(df) == 0:
        st.warning("No hay datos cargados. Sube un CSV en el panel lateral.")
        return

    ana = df[_as_bool(df["incluir_analisis"])] if "incluir_analisis" in df.columns else df
    n_total, n_ana = len(df), len(ana)

    st.title("HemoVet - GENVET-VH50")
    st.subheader("Perfil de salud hematológica de la población atendida")

    periodo = ""
    if "fecha" in ana.columns:
        fechas = pd.to_datetime(ana["fecha"], errors="coerce").dropna()
        if not fechas.empty:
            periodo = f"{fechas.min():%m/%Y} – {fechas.max():%m/%Y}"
    n_especies = ana["especie"].nunique() if "especie" in ana.columns else 0

    st.write(
        f"Análisis de **{n_total} muestras** de hemograma veterinario "
        f"({n_especies} especies" + (f", {periodo}" if periodo else "") + "). "
        f"La **población de análisis** es de **{n_ana} muestras**, tras excluir "
        "antecedentes y muestras sin hemograma."
    )

    pct_anemia = _as_bool(ana["f_anemia"]).mean() * 100 if "f_anemia" in ana.columns else 0
    flags = [c for c in FLAGS_RELEVANTES if c in ana.columns]
    pct_otra = ana[flags].apply(_as_bool).any(axis=1).mean() * 100 if flags else 0
    especie_top = (
        ana["especie"].mode().iloc[0]
        if "especie" in ana.columns and not ana["especie"].dropna().empty else "—"
    )
    st.divider()
    _subtitulo("Panorama general")
    c1, c2, c3, c4 = st.columns(4)
    _kpi(c1, "Muestras analizadas", f"{n_ana}")
    _kpi(c2, "Con anemia", f"{pct_anemia:.0f} %", color=ACENTO) 
    _kpi(c3, "Con otra alteración", f"{pct_otra:.0f} %")
    _kpi(c4, "Especie más frecuente", str(especie_top))
    st.divider()

    

