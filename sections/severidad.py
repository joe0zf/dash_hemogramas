import streamlit as st
import pandas as pd
import plotly.express as px


def render(df):
    st.title("Severidad de la Anemia")
    st.write("Análisis de la gravedad en los pacientes diagnosticados con anemia.")

    if df is None or df.empty:
        st.info("Carga un dataset desde el menú lateral para visualizar esta sección.")
        return

    df_trabajo = df.copy()
    if "incluir_analisis" in df_trabajo.columns:
        solo_validos = st.checkbox("Incluir solo registros válidos para análisis", value=True)
        if solo_validos:
            df_trabajo = df_trabajo[df_trabajo["incluir_analisis"] == True]

    df_anemia = df_trabajo[df_trabajo["tiene_anemia"] == "Sí"].copy()

    if df_anemia.empty:
        st.warning("No se encontraron registros con anemia en el dataset filtrado.")
        return

    colores = {
        "Leve": "#F1C40F",
        "Moderada": "#E67E22",
        "Severa": "#E74C3C",
        "No clasificada (sin valor)": "#95A5A6",
        "Sin anemia": "#2ECC71"
    }

    total_anemia = len(df_anemia)
    leves = len(df_anemia[df_anemia["severidad_anemia"] == "Leve"])
    moderadas = len(df_anemia[df_anemia["severidad_anemia"] == "Moderada"])
    severas = len(df_anemia[df_anemia["severidad_anemia"] == "Severa"])
    no_clasificadas = len(df_anemia[df_anemia["severidad_anemia"] == "No clasificada (sin valor)"])

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total con Anemia", total_anemia)
    c2.metric("Anemia Leve", leves)
    c3.metric("Anemia Moderada", moderadas)
    c4.metric("Anemia Severa", severas)
    c5.metric("No clasificada", no_clasificadas)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribución por Severidad")
        conteo = df_anemia["severidad_anemia"].value_counts().reset_index()
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
        st.subheader("Hemoglobina (g/dL) en Pacientes con Anemia")
        df_hgb = df_anemia.dropna(subset=["HGB (g/dL)"])
        if not df_hgb.empty:
            fig_box = px.box(
                df_hgb,
                x="especie",
                y="HGB (g/dL)",
                color="severidad_anemia",
                points="all",
                color_discrete_map=colores
            )
            st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.info("No hay valores numéricos de HGB (g/dL) registrados para los casos seleccionados.")

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Severidad por Especie")
        resumen_especie = (
            df_anemia.groupby(["especie", "severidad_anemia"])
            .size()
            .reset_index(name="Casos")
        )

        fig_especie = px.bar(
            resumen_especie,
            x="especie",
            y="Casos",
            color="severidad_anemia",
            barmode="group",
            color_discrete_map=colores
        )
        st.plotly_chart(fig_especie, use_container_width=True)

    with col4:
        st.subheader("Severidad por Grupo Etario")
        resumen_edad = (
            df_anemia.groupby(["grupo_etario", "severidad_anemia"])
            .size()
            .reset_index(name="Casos")
        )

        fig_edad = px.bar(
            resumen_edad,
            x="grupo_etario",
            y="Casos",
            color="severidad_anemia",
            barmode="group",
            color_discrete_map=colores
        )
        st.plotly_chart(fig_edad, use_container_width=True)

    st.subheader("Detalle de pacientes con anemia")
    filtro_grado = st.selectbox(
        "Filtrar tabla por categoría de severidad:",
        options=["Todos"] + list(df_anemia["severidad_anemia"].unique())
    )

    df_tabla = df_anemia if filtro_grado == "Todos" else df_anemia[df_anemia["severidad_anemia"] == filtro_grado]

    columnas_tabla = [
        "ID muestra", "Nombre", "fecha", "especie", "sexo",
        "grupo_etario", "HGB (g/dL)", "RBC (10^12/L)", "MCV (fL)",
        "tipo_anemia", "cromia", "severidad_anemia"
    ]
    st.dataframe(df_tabla[columnas_tabla], use_container_width=True, hide_index=True)
