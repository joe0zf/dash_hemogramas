import streamlit as st
import pandas as pd

FLAGS_RELEVANTES = [
    "f_microcitosis", "f_macrocitosis", "f_mchc_baja", "f_eritrocitosis",
    "f_leucopenia", "f_leucocitosis", "f_linfopenia", "f_linfocitosis",
    "f_neu_alto", "f_neu_bajo", "f_trombocitopenia", "f_trombocitosis",
]

PASOS = [
    ("1 · Prevalencia",    "¿Qué tan común es la anemia?"),
    ("2 · Tipo de anemia", "¿De qué tipo es?"),
    ("3 · Concentración",  "¿En quién se concentra?"),
    ("4 · Severidad",      "¿Quiénes requieren atención?"),
]


def _as_bool(serie: pd.Series) -> pd.Series:
    return serie.astype(str).str.lower().isin(["true", "1"])


def render(df) -> None:
    if df is None or len(df) == 0:
        st.warning("No hay datos cargados. Sube un CSV en el panel lateral.")
        return
    ana = df[_as_bool(df["incluir_analisis"])] if "incluir_analisis" in df.columns else df
    n_total, n_ana = len(df), len(ana)

    st.title("HemoVet — Bethoven")
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

    st.markdown("#### Panorama general")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Muestras analizadas", f"{n_ana}")
    c2.metric("Con anemia", f"{pct_anemia:.0f} %")
    c3.metric(
        "Con otra alteración", f"{pct_otra:.0f} %",
        help="Excluye la bandera 'MCHC alta', marcada en casi todas las muestras "
             "por un posible problema de calibración.",
    )
    c4.metric("Especie más frecuente", especie_top)

    st.divider()

    st.markdown("#### Cómo recorrer el dashboard")
    st.caption("El análisis sigue cuatro pasos. Usa el **menú principal** del panel lateral.")
    cols = st.columns(4)
    for col, (titulo, pregunta) in zip(cols, PASOS):
        with col:
            st.markdown(f"**{titulo}**")
            st.caption(pregunta)

    st.divider()