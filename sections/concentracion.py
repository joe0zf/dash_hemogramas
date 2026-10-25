import streamlit as st
import pandas as pd
import plotly.express as px


def render(df):
    st.title("Concentración de Hemoglobina y Cromía")
    st.write("Análisis de los niveles de hemoglobina (HGB) y concentración corpuscular en la población.")

    if df is None or df.empty:
        return

    st.sidebar.subheader("Sobre la Concentración")
    st.sidebar.info(
        "Evalúa la cantidad de hemoglobina en sangre (g/dL) y su concentración dentro del eritrocito (cromía)."
    )

    df_anemia = df[df["tiene_anemia"] == "Sí"].copy()
    df_hgb = df.dropna(subset=["HGB (g/dL)"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("HGB Promedio (Sano)", f"{df_hgb[df_hgb['tiene_anemia'] == 'No']['HGB (g/dL)'].mean():.1f} g/dL")
    c2.metric("HGB Promedio (Anemia)", f"{df_hgb[df_hgb['tiene_anemia'] == 'Sí']['HGB (g/dL)'].mean():.1f} g/dL")
    c3.metric("Normocrómica", int((df_anemia["cromia"] == "Normocrómica").sum()))
    c4.metric("Hipercrómica / Hipocrómica", int((df_anemia["cromia"] != "Normocrómica").sum()))

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Nivel de Hemoglobina: Sanos vs Anemia")
        df_hgb_val = df_hgb[df_hgb["HGB (g/dL)"] > 1.0]

        fig_box = px.box(
            df_hgb_val,
            x="especie",
            y="HGB (g/dL)",
            color="tiene_anemia",
            points="all",
            color_discrete_map={"No": "#2ECC71", "Sí": "#E74C3C"},
            labels={"especie": "Especie", "HGB (g/dL)": "Hemoglobina (g/dL)", "tiene_anemia": "Anemia"}
        )
        fig_box.update_layout(boxmode="group")
        st.plotly_chart(fig_box, use_container_width=True)

    with col2:
        st.subheader("Mapa de Cromía por Especie (Pacientes con Anemia)")
        resumen_cromia = df_anemia.groupby(["especie", "cromia"]).size().reset_index(name="Casos")

        fig_tree = px.treemap(
            resumen_cromia,
            path=["especie", "cromia"],
            values="Casos",
            color="cromia",
            color_discrete_map={
                "Hipocrómica": "#E67E22",
                "Normocrómica": "#2ECC71",
                "Hipercrómica": "#3498DB"
            }
        )
        st.plotly_chart(fig_tree, use_container_width=True)
