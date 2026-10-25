import streamlit as st
import streamlit as st
import pandas as pd
import plotly.express as px


def show(df):
    st.title("Severidad de la Anemia")
    st.write("Análisis de la gravedad en los pacientes diagnosticados.")

    st.sidebar.subheader("Sobre la Severidad")
    st.sidebar.info(
        "Leve: Requiere control y mejora nutricional.\n\n"
        "Moderada: Necesita tratamiento y seguimiento.\n\n"
        "Severa: Caso crítico de atención prioritaria."
    )

    grados = ["Leve", "Moderada", "Severa"]
    df_anemia = df[df["severidad"].isin(grados)]

    colores = {
        "Leve": "#F1C40F",
        "Moderada": "#E67E22",
        "Severa": "#E74C3C"
    }

    total = len(df_anemia)
    leves = len(df_anemia[df_anemia["severidad"] == "Leve"])
    moderadas = len(df_anemia[df_anemia["severidad"] == "Moderada"])
    severas = len(df_anemia[df_anemia["severidad"] == "Severa"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total con Anemia", total)
    c2.metric("Anemia Leve", leves)
    c3.metric("Anemia Moderada", moderadas)
    c4.metric("Anemia Severa", severas)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Porcentaje por Severidad")
        conteo = df_anemia["severidad"].value_counts().reset_index()
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
            x="severidad",
            y="hemoglobina",
            color="severidad",
            color_discrete_map=colores
        )
        st.plotly_chart(fig_box, use_container_width=True)

    st.subheader("Severidad según Sexo")
    resumen_sexo = df_anemia.groupby(["sexo", "severidad"]).size().reset_index(name="Casos")

    fig_bar = px.bar(
        resumen_sexo,
        x="sexo",
        y="Casos",
        color="severidad",
        barmode="group",
        color_discrete_map=colores
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("Casos severos")
    df_severos = df_anemia[df_anemia["severidad"] == "Severa"]
    st.dataframe(df_severos)

def render() -> None:
    st.header("Sobre nosotros")
    st.write("Esta aplicación reúne herramientas para revisar y analizar hemogramas en animales.")
