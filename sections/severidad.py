import streamlit as st
import pandas as pd
import plotly.express as px


def clasificar_severidad(row):
    hgb = row["HGB (g/dL)"]
    n_alt = row["n_alteraciones"]

    if pd.notna(hgb):
        if hgb < 10.0:
            return "Severa"
        elif hgb < 12.0:
            return "Moderada"
        return "Leve"

    if n_alt >= 5:
        return "Severa"
    elif n_alt >= 3:
        return "Moderada"
    return "Leve"


def render(df):
    st.title("Severidad de la Anemia")
    st.write("Gravedad clínica de los pacientes diagnosticados con anemia.")

    if df is None or df.empty:
        return

    st.sidebar.subheader("Sobre la Severidad")
    st.sidebar.info(
        "Leve: Control y ajuste nutricional.\n\n"
        "Moderada: Tratamiento y monitoreo.\n\n"
        "Severa: Atención clínica prioritaria."
    )

    df_anemia = df[df["tiene_anemia"] == "Sí"].copy()
    df_anemia["severidad"] = df_anemia.apply(clasificar_severidad, axis=1)

    grados = ["Leve", "Moderada", "Severa"]
    colores = {"Leve": "#F1C40F", "Moderada": "#E67E22", "Severa": "#E74C3C"}

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total con Anemia", len(df_anemia))
    c2.metric("Leve", int((df_anemia["severidad"] == "Leve").sum()))
    c3.metric("Moderada", int((df_anemia["severidad"] == "Moderada").sum()))
    c4.metric("Severa", int((df_anemia["severidad"] == "Severa").sum()))

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Casos por Nivel de Severidad")
        conteo = df_anemia["severidad"].value_counts().reindex(grados, fill_value=0).reset_index()
        conteo.columns = ["Severidad", "Casos"]

        fig_bar_h = px.bar(
            conteo,
            x="Casos",
            y="Severidad",
            color="Severidad",
            orientation="h",
            text_auto=True,
            color_discrete_map=colores
        )
        fig_bar_h.update_layout(showlegend=False)
        st.plotly_chart(fig_bar_h, use_container_width=True)

    with col2:
        st.subheader("Proporción de Severidad según Especie")
        resumen_esp = df_anemia.groupby(["especie", "severidad"]).size().reset_index(name="Casos")

        fig_stack = px.bar(
            resumen_esp,
            x="especie",
            y="Casos",
            color="severidad",
            barmode="stack",
            text_auto=True,
            color_discrete_map=colores,
            category_orders={"severidad": grados}
        )
        st.plotly_chart(fig_stack, use_container_width=True)
