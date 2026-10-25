import streamlit as st
import pandas as pd
import plotly.express as px

ACENTO = "#C0392B"   # rojo: anemia
GRIS   = "#CFD2D6"   # gris: datos auxiliares

FLAGS_PANORAMA = {
    "f_anemia": "Anemia",
    "f_linfopenia": "Linfopenia",
    "f_neu_bajo": "Neutropenia",
    "f_trombocitopenia": "Trombocitopenia",
    "f_leucopenia": "Leucopenia",
    "f_microcitosis": "Microcitosis",
    "f_macrocitosis": "Macrocitosis",
    "f_mchc_baja": "MCHC baja",
    "f_eritrocitosis": "Eritrocitosis",
    "f_leucocitosis": "Leucocitosis",
    "f_linfocitosis": "Linfocitosis",
    "f_neu_alto": "Neutrofilia",
    "f_trombocitosis": "Trombocitosis",
}


def _as_bool(serie: pd.Series) -> pd.Series:
    return serie.astype(str).str.lower().isin(["true", "1"])


def _subtitulo(texto_html: str) -> None:
    st.markdown(
        f"<p style='font-size:1.05rem; font-weight:600; margin-bottom:0.3rem'>{texto_html}</p>",
        unsafe_allow_html=True,
    )


def render(df) -> None:
    if df is None or len(df) == 0:
        st.warning("No hay datos cargados. Sube un CSV en el panel lateral.")
        return

    ana = df[_as_bool(df["incluir_analisis"])] if "incluir_analisis" in df.columns else df
    n = len(ana)
    if n == 0:
        st.warning("No hay muestras en la población de análisis con los filtros actuales.")
        return

    con_anemia = int(_as_bool(ana["f_anemia"]).sum())
    pct = con_anemia / n * 100 if n else 0
    uno_de_cada = round(100 / pct) if pct else 0

    st.title("Prevalencia")
    st.caption(f"1 de cada {uno_de_cada} pacientes llega con anemia")
    st.divider()

    col_izq, col_der = st.columns(2)

    with col_izq:
        _subtitulo(
            f"El {pct:.0f}% de los pacientes presenta "
            f"<span style='color:{ACENTO}'>anemia</span>"
        )
        prev = pd.DataFrame({
            "estado": ["Con anemia", "Sin anemia"],
            "n": [con_anemia, n - con_anemia],
        })
        fig = px.pie(
            prev, names="estado", values="n", hole=0.62,
            color="estado",
            color_discrete_map={"Con anemia": ACENTO, "Sin anemia": GRIS},
        )
        fig.update_traces(
            textinfo="none", sort=False,
            hovertemplate="%{label}: %{value} muestras (%{percent})<extra></extra>",
        )
        fig.update_layout(
            height=360, margin=dict(t=10, b=40, l=10, r=10),
            showlegend=True,
            legend=dict(orientation="h", y=-0.08, x=0.5, xanchor="center"),
            annotations=[dict(text=f"{pct:.0f}%", x=0.5, y=0.5,
                              font=dict(size=46, color=ACENTO), showarrow=False)],
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_der:
        _subtitulo("La anemia encabeza las alteraciones de la clínica")
        registros = [
            (label, int(_as_bool(ana[col]).sum()))
            for col, label in FLAGS_PANORAMA.items() if col in ana.columns
        ]
        panorama = (
            pd.DataFrame(registros, columns=["alteracion", "n"])
            .query("n > 0").sort_values("n")
        )
        panorama["foco"] = panorama["alteracion"].eq("Anemia").map(
            {True: "Anemia", False: "Otras"}
        )
        figb = px.bar(
            panorama, x="n", y="alteracion", orientation="h", text="n",
            color="foco", color_discrete_map={"Anemia": ACENTO, "Otras": GRIS},
        )
        figb.update_traces(textposition="outside")
        figb.update_layout(
            showlegend=False, height=360, margin=dict(t=10, b=40, l=10, r=10),
            xaxis_title="", yaxis_title="",
            xaxis=dict(showgrid=False, showticklabels=False),
            hovermode=False,
        )
        st.plotly_chart(figb, use_container_width=True)

    st.divider()
