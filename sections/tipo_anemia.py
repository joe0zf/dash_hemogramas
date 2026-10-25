import streamlit as st
import pandas as pd
import plotly.express as px

RANGOS_ESPECIE = {
    "Perro": {"mcv_min": 61.5, "mcv_max": 67.0},
    "Gato": {"mcv_min": 39.5, "mcv_max": 46.5},
    "Oveja": {"mcv_min": 28.5, "mcv_max": 32.0},
    "Vaca": {"mcv_min": 40.0, "mcv_max": 60.0},
    "Caballo": {"mcv_min": 37.0, "mcv_max": 58.0},
    "Mono": {"mcv_min": 65.0, "mcv_max": 85.0}
}

def clasificar_tipo_morfologico(row):

    if row["tiene_anemia"] != "Sí":
        return "Sin anemia"

    esp = row["especie"]
    mcv = row["MCV (fL)"]

    limites = RANGOS_ESPECIE.get(esp)

    if limites and pd.notna(mcv):

        if mcv < limites["mcv_min"]:
            return "Microcítica"

        elif mcv > limites["mcv_max"]:
            return "Macrocítica"

        else:
            return "Normocítica"

    return "Normocítica"


def render(df):

    st.title("Clasificación Morfológica de la Anemia")

    st.write(
        "Tipificación según el Volumen Corpuscular Medio (MCV) para cada especie."
    )

    if df is None or df.empty:
        st.info(
            "Carga un dataset desde el menú lateral para visualizar esta sección."
        )
        return

    st.sidebar.subheader("Sobre el Tipo de Anemia")

    st.sidebar.info(
        "Microcítica: Eritrocitos más pequeños que el rango de referencia.\n\n"
        "Normocítica: Eritrocitos dentro del rango normal.\n\n"
        "Macrocítica: Eritrocitos más grandes que el rango de referencia."
    )

    df_proc = df.copy()

    df_proc["tipo_anemia"] = df_proc.apply(
        clasificar_tipo_morfologico,
        axis=1
    )

    tipos = [
        "Microcítica",
        "Normocítica",
        "Macrocítica"
    ]

    df_anemia = df_proc[
        df_proc["tipo_anemia"].isin(tipos)
    ]

    colores_tipo = {
        "Microcítica": "#3498DB",
        "Normocítica": "#2ECC71",
        "Macrocítica": "#9B59B6"
    }

    total = len(df_anemia)

    micro = len(
        df_anemia[df_anemia["tipo_anemia"] == "Microcítica"]
    )

    normo = len(
        df_anemia[df_anemia["tipo_anemia"] == "Normocítica"]
    )

    macro = len(
        df_anemia[df_anemia["tipo_anemia"] == "Macrocítica"]
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total con Anemia", total)
    c2.metric("Microcítica", micro)
    c3.metric("Normocítica", normo)
    c4.metric("Macrocítica", macro)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Frecuencia de Tipos de Anemia")

        conteo = (
            df_anemia["tipo_anemia"]
            .value_counts()
            .reindex(tipos, fill_value=0)
            .reset_index()
        )

        conteo.columns = ["Tipo", "Casos"]

        fig_tipo = px.bar(
            conteo,
            y="Tipo",
            x="Casos",
            orientation="h",
            text="Casos",
            color="Tipo",
            color_discrete_map=colores_tipo
        )

        fig_tipo.update_traces(
            textposition="outside"
        )

        fig_tipo.update_layout(
            showlegend=False,
            xaxis_title="Número de casos",
            yaxis_title="",
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig_tipo,
            use_container_width=True
        )

    with col2:

        st.subheader("Tipo de Anemia según Especie")

        tabla_heatmap = pd.crosstab(
            df_anemia["especie"],
            df_anemia["tipo_anemia"]
        )

        tabla_heatmap = tabla_heatmap.reindex(
            columns=tipos,
            fill_value=0
        )

        fig_heatmap = px.imshow(
            tabla_heatmap,
            text_auto=True,
            color_continuous_scale="Blues",
            aspect="auto"
        )

        fig_heatmap.update_layout(
            xaxis_title="Tipo de anemia",
            yaxis_title="Especie",
            coloraxis_colorbar_title="Casos",
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig_heatmap,
            use_container_width=True
        )
