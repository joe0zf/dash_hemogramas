import streamlit as st
import pandas as pd
import plotly.express as px


def render(df):
    st.title("Severidad de la Anemia")
    st.write("Análisis de la gravedad en los pacientes diagnosticados.")

    if df is None or df.empty:
        st.info("Carga un dataset desde el menú lateral para visualizar esta sección.")
        return

    col_severidad = "severidad_anemia"
    col_hb = "HGB (g/dL)"
    col_especie = "especie"
    col_edad = "grupo_etario"

    grados = ["Leve", "Moderada", "Severa"]
    df_anemia = df[df[col_severidad].isin(grados)]

    if df_anemia.empty:
        df_anemia = df[df["f_anemia"] == 1] if "f_anemia" in df.columns else df.dropna(subset=[col_severidad])

    colores = {
        "Leve": "#F1C40F",
        "Moderada": "#E67E22",
        "Severa": "#E74C3C"
    }

    total = len(df_anemia)
    leves = len(df_anemia[df_anemia[col_severidad] == "Leve"])
    moderadas = len(df_anemia[df_anemia[col_severidad] == "Moderada"])
    severas = len(df_anemia[df_anemia[col_severidad] == "Severa"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total con Anemia", total)
    c2.metric("Anemia Leve", leves)
    c3.metric("Anemia Moderada", moderadas)
    c4.metric("Anemia Severa", severas)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Porcentaje por Severidad")
        conteo = df_anemia[col_severidad].value_counts().reset_index()
        conteo.columns = ["Severidad", "Cantidad"]

        fig_pie = px.pie(
            conteo,
            names="Severidad",
            values="Cantidad",
            color="Severidad",
            color_discrete_map=colores,
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("Hemoglobina según Severidad")
        fig_box = px.box(
            df_anemia,
            x=col_severidad,
            y=col_hb,
            color=col_severidad,
            color_discrete_map=colores
        )
        st.plotly_chart(fig_box, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Severidad por Especie")
        resumen_especie = df_anemia.groupby([col_especie, col_severidad]).size().reset_index(name="Casos")

        fig_especie = px.bar(
            resumen_especie,
            x=col_especie,
            y="Casos",
            color=col_severidad,
            barmode="group",
            color_discrete_map=colores
        )
        st.plotly_chart(fig_especie, use_container_width=True)

    with col4:
        st.subheader("Severidad por Grupo Etario")
        resumen_edad = df_anemia.groupby([col_edad, col_severidad]).size().reset_index(name="Casos")

        fig_edad = px.bar(
            resumen_edad,
            x=col_edad,
            y="Casos",
            color=col_severidad,
            barmode="group",
            color_discrete_map=colores
        )
        st.plotly_chart(fig_edad, use_container_width=True)

    st.subheader("Registros de casos severos")
    columnas_tabla = ["ID muestra", "Nombre", "fecha", "especie", "sexo", "grupo_etario", "HGB (g/dL)", "HCT (%)", "tipo_anemia", "severidad_anemia"]
    df_severos = df_anemia[df_anemia[col_severidad] == "Severa"]
    st.dataframe(df_severos[columnas_tabla], use_container_width=True, hide_index=True)
