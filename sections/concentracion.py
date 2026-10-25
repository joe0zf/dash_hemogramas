import streamlit as st


def render() -> None:
    st.header("Información")
    st.write("Este panel permite consultar y explorar datos de hemogramas en animales.")
import streamlit as st
import pandas as pd
import plotly.express as px


def render(df):
    st.title("Concentración y Cromía de la Anemia")
    st.write("Evaluación de la concentración corpuscular de hemoglobina basada en los hallazgos del hemograma.")

    if df is None or df.empty:
        st.info("Carga un dataset desde el menú lateral para visualizar esta sección.")
        return

    st.sidebar.subheader("Sobre la Concentración")
    st.sidebar.info(
        "Hipocrómica: Disminución de la concentración de hemoglobina corpuscular.\n\n"
        "Normocrómica: Concentración dentro de los parámetros esperados.\n\n"
        "Hipercrómica: Elevación en la concentración de hemoglobina según los criterios del laboratorio."
    )

    df_anemia = df[df["tiene_anemia"] == "Sí"].copy()

    if df_anemia.empty:
        st.warning("No se encontraron registros con anemia en el dataset.")
        return

    colores_cromia = {
        "Hipocrómica": "#E67E22",
        "Normocrómica": "#2ECC71",
        "Hipercrómica": "#3498DB"
    }

    total = len(df_anemia)
    hipo = len(df_anemia[df_anemia["cromia"] == "Hipocrómica"])
    normo = len(df_anemia[df_anemia["cromia"] == "Normocrómica"])
    hiper = len(df_anemia[df_anemia["cromia"] == "Hipercrómica"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total con Anemia", total)
    c2.metric("Hipocrómica", hipo)
    c3.metric("Normocrómica", normo)
    c4.metric("Hipercrómica", hiper)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribución Porcentual de la Cromía")
        conteo = df_anemia["cromia"].value_counts().reset_index()
        conteo.columns = ["Cromía", "Cantidad"]

        fig_pie = px.pie(
            conteo,
            names="Cromía",
            values="Cantidad",
            color="Cromía",
            color_discrete_map=colores_cromia,
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("Cromía según Especie")
        resumen_especie = (
            df_anemia.groupby(["especie", "cromia"])
            .size()
            .reset_index(name="Casos")
        )

        fig_especie = px.bar(
            resumen_especie,
            x="especie",
            y="Casos",
            color="cromia",
            barmode="group",
            color_discrete_map=colores_cromia
        )
        st.plotly_chart(fig_especie, use_container_width=True)

    st.subheader("Banderas de Alteración MCHC (Dataset)")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        n_alta = df_anemia["f_mchc_alta"].sum()
        st.metric("Registros con MCHC Alta / Hipercrómica", int(n_alta))
    with col_b2:
        n_baja = df_anemia["f_mchc_baja"].sum()
        st.metric("Registros con MCHC Baja / Hipocrómica", int(n_baja))

    st.subheader("Detalle de pacientes anémicos por cromía")
    filtro_cromia = st.selectbox(
        "Filtrar tabla por tipo de cromía:",
        options=["Todos"] + list(df_anemia["cromia"].unique())
    )

    df_tabla = df_anemia if filtro_cromia == "Todos" else df_anemia[df_anemia["cromia"] == filtro_cromia]

    columnas_tabla = [
        "ID muestra", "Nombre", "fecha", "especie", "sexo",
        "grupo_etario", "MCH (pg)", "MCHC (g/dL)", "tipo_anemia", "cromia"
    ]
    st.dataframe(df_tabla[columnas_tabla], use_container_width=True, hide_index=True)
