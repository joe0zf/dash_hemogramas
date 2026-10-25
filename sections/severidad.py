import streamlit as st
import pandas as pd
import plotly.express as px


def clasificar_severidad(row):
    if row["tiene_anemia"] != "Sí":
        return "Sin anemia"

    hgb = row["HGB (g/dL)"]
    esp = row["especie"]
    n_alt = row["n_alteraciones"]

    if pd.notna(hgb):
        if esp == "Perro":
            if hgb < 11.8:
                return "Severa"
            elif hgb < 12.5:
                return "Moderada"
            else:
                return "Leve"
        elif esp == "Gato":
            if hgb < 9.5:
                return "Severa"
            elif hgb < 11.0:
                return "Moderada"
            else:
                return "Leve"
        else:
            if hgb < 7.0:
                return "Severa"
            elif hgb < 9.0:
                return "Moderada"
            else:
                return "Leve"

    if n_alt >= 5:
        return "Severa"
    elif n_alt >= 3:
        return "Moderada"
    else:
        return "Leve"


def render(df):
    st.title("Severidad de la Anemia")
    st.write("Análisis de la gravedad en los pacientes diagnosticados.")

    if df is None or df.empty:
        st.info("Carga un dataset desde el menú lateral para visualizar esta sección.")
        return

    st.sidebar.subheader("Sobre la Severidad")
    st.sidebar.info(
        "Leve: Requiere control y mejora nutricional.\n\n"
        "Moderada: Necesita tratamiento y seguimiento.\n\n"
        "Severa: Caso crítico de atención prioritaria."
    )

    df_proc = df.copy()
    df_proc["severidad_anemia"] = df_proc.apply(clasificar_severidad, axis=1)

    grados = ["Leve", "Moderada", "Severa"]
    df_anemia = df_proc[df_proc["severidad_anemia"].isin(grados)]

    colores = {
        "Leve": "#F1C40F",
        "Moderada": "#E67E22",
        "Severa": "#E74C3C"
    }

    total = len(df_anemia)
    leves = len(df_anemia[df_anemia["severidad_anemia"] == "Leve"])
    moderadas = len(df_anemia[df_anemia["severidad_anemia"] == "Moderada"])
    severas = len(df_anemia[df_anemia["severidad_anemia"] == "Severa"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total con Anemia", total)
    c2.metric("Anemia Leve", leves)
    c3.metric("Anemia Moderada", moderadas)
    c4.metric("Anemia Severa", severas)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Porcentaje por Severidad")
        conteo = (
            df_anemia["severidad_anemia"]
            .value_counts()
            .reindex(grados, fill_value=0)
            .reset_index()
        )
        conteo.columns = ["Severidad", "Cantidad"]

        fig_pie = px.pie(
            conteo,
            names="Severidad",
            values="Cantidad",
            color="Severidad",
            color_discrete_map=colores,
            category_orders={"Severidad": grados},
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("Hemoglobina según Severidad")
        df_hgb = df_anemia.dropna(subset=["HGB (g/dL)"])
        fig_box = px.box(
            df_hgb,
            x="severidad_anemia",
            y="HGB (g/dL)",
            color="severidad_anemia",
            color_discrete_map=colores,
            category_orders={"severidad_anemia": grados}
        )
        st.plotly_chart(fig_box, use_container_width=True)

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
            color_discrete_map=colores,
            category_orders={"severidad_anemia": grados}
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
            color_discrete_map=colores,
            category_orders={"severidad_anemia": grados}
        )
        st.plotly_chart(fig_edad, use_container_width=True)

    st.subheader("Casos severos")
    columnas_tabla = [
        "ID muestra", "Nombre", "fecha", "especie", "sexo",
        "grupo_etario", "HGB (g/dL)", "n_alteraciones", "tipo_anemia", "severidad_anemia"
    ]
    df_severos = df_anemia[df_anemia["severidad_anemia"] == "Severa"]
    st.dataframe(df_severos[columnas_tabla], use_container_width=True, hide_index=True)
