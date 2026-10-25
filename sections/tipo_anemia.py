import streamlit as st
import pandas as pd
import plotly.express as px


RANGOS_ESPECIE = {
    "Perro": {"mcv_min": 61.5, "mcv_max": 67.0, "mch_min": 22.5, "mch_max": 26.8, "mchc_min": 32.0, "mchc_max": 36.0},
    "Gato": {"mcv_min": 39.5, "mcv_max": 46.5, "mch_min": 13.0, "mch_max": 17.5, "mchc_min": 30.0, "mchc_max": 36.0},
    "Oveja": {"mcv_min": 28.5, "mcv_max": 32.0, "mch_min": 10.8, "mch_max": 12.0, "mchc_min": 31.0, "mchc_max": 35.0},
    "Vaca": {"mcv_min": 40.0, "mcv_max": 60.0, "mch_min": 14.0, "mch_max": 24.0, "mchc_min": 30.0, "mchc_max": 36.0},
    "Caballo": {"mcv_min": 37.0, "mcv_max": 58.0, "mch_min": 12.0, "mch_max": 19.0, "mchc_min": 31.0, "mchc_max": 38.0},
    "Mono": {"mcv_min": 65.0, "mcv_max": 85.0, "mch_min": 20.0, "mch_max": 28.0, "mchc_min": 30.0, "mchc_max": 36.0}
}


def clasificar_tipo_morfologico(row):
    if row["tiene_anemia"] != "Sí":
        return "Sin anemia"

    if row.get("f_microcitosis") == True:
        return "Microcítica"
    if row.get("f_macrocitosis") == True:
        return "Macrocítica"

    esp = row["especie"]
    mcv = row["MCV (fL)"]
    mch = row["MCH (pg)"]
    limites = RANGOS_ESPECIE.get(esp)

    if limites:
        if pd.notna(mcv):
            if mcv < limites["mcv_min"]:
                return "Microcítica"
            elif mcv > limites["mcv_max"]:
                return "Macrocítica"
            else:
                return "Normocítica"

        if pd.notna(mch):
            if mch < limites["mch_min"]:
                return "Microcítica"
            elif mch > limites["mch_max"]:
                return "Macrocítica"
            else:
                return "Normocítica"

    return row["tipo_anemia"]


def clasificar_cromia(row):
    if row["tiene_anemia"] != "Sí":
        return "Sin anemia"

    if row.get("f_mchc_baja") == True:
        return "Hipocrómica"
    if row.get("f_mchc_alta") == True:
        return "Hipercrómica"

    esp = row["especie"]
    mchc = row["MCHC (g/dL)"]
    mch = row["MCH (pg)"]
    limites = RANGOS_ESPECIE.get(esp)

    if limites:
        if pd.notna(mchc):
            if mchc < limites["mchc_min"]:
                return "Hipocrómica"
            elif mchc > limites["mchc_max"]:
                return "Hipercrómica"
            else:
                return "Normocrómica"

        if pd.notna(mch):
            if mch < limites["mch_min"]:
                return "Hipocrómica"
            elif mch > limites["mch_max"]:
                return "Hipercrómica"
            else:
                return "Normocrómica"

    return row["cromia"]


def render(df):
    st.title("Clasificación Morfológica de la Anemia")
    st.write("Tipificación según el Volumen Corpuscular Medio (MCV) y la concentración de hemoglobina por especie.")

    if df is None or df.empty:
        st.info("Carga un dataset desde el menú lateral para visualizar esta sección.")
        return

    st.sidebar.subheader("Sobre el Tipo de Anemia")
    st.sidebar.info(
        "Microcítica: Eritrocitos de menor tamaño al rango de la especie (asociada a deficiencia de hierro o pérdida crónica).\n\n"
        "Normocítica: Eritrocitos de volumen normal (frecuente en procesos inflamatorios, infecciosos o hemorragia aguda).\n\n"
        "Macrocítica: Eritrocitos de mayor volumen (indicativo de respuesta regenerativa con reticulocitosis o alteraciones en la maduración)."
    )

    df_proc = df.copy()
    df_proc["tipo_anemia"] = df_proc.apply(clasificar_tipo_morfologico, axis=1)
    df_proc["cromia"] = df_proc.apply(clasificar_cromia, axis=1)

    tipos = ["Microcítica", "Normocítica", "Macrocítica"]
    df_anemia = df_proc[df_proc["tipo_anemia"].isin(tipos)]

    colores_tipo = {
        "Microcítica": "#3498DB",
        "Normocítica": "#2ECC71",
        "Macrocítica": "#9B59B6"
    }

    total = len(df_anemia)
    micro = len(df_anemia[df_anemia["tipo_anemia"] == "Microcítica"])
    normo = len(df_anemia[df_anemia["tipo_anemia"] == "Normocítica"])
    macro = len(df_anemia[df_anemia["tipo_anemia"] == "Macrocítica"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total con Anemia", total)
    c2.metric("Anemia Microcítica", micro)
    c3.metric("Anemia Normocítica", normo)
    c4.metric("Anemia Macrocítica", macro)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Proporción por Tipo de Anemia")
        conteo = (
            df_anemia["tipo_anemia"]
            .value_counts()
            .reindex(tipos, fill_value=0)
            .reset_index()
        )
        conteo.columns = ["Tipo", "Cantidad"]

        fig_pie = px.pie(
            conteo,
            names="Tipo",
            values="Cantidad",
            color="Tipo",
            color_discrete_map=colores_tipo,
            category_orders={"Tipo": tipos},
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("Distribución de MCV (fL) por Especie")
        df_mcv = df_anemia.dropna(subset=["MCV (fL)"])
        fig_box = px.box(
            df_mcv,
            x="especie",
            y="MCV (fL)",
            color="tipo_anemia",
            color_discrete_map=colores_tipo,
            category_orders={"tipo_anemia": tipos}
        )
        st.plotly_chart(fig_box, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Tipo de Anemia según Especie")
        resumen_especie = (
            df_anemia.groupby(["especie", "tipo_anemia"])
            .size()
            .reset_index(name="Casos")
        )

        fig_especie = px.bar(
            resumen_especie,
            x="especie",
            y="Casos",
            color="tipo_anemia",
            barmode="group",
            color_discrete_map=colores_tipo,
            category_orders={"tipo_anemia": tipos}
        )
        st.plotly_chart(fig_especie, use_container_width=True)

    with col4:
        st.subheader("Relación Morfología vs Cromía")
        resumen_cromia = (
            df_anemia.groupby(["tipo_anemia", "cromia"])
            .size()
            .reset_index(name="Casos")
        )

        fig_cromia = px.bar(
            resumen_cromia,
            x="tipo_anemia",
            y="Casos",
            color="cromia",
            barmode="group",
            category_orders={"tipo_anemia": tipos}
        )
        st.plotly_chart(fig_cromia, use_container_width=True)

    st.subheader("Intervalos de referencia utilizados por especie")
    df_ref = pd.DataFrame([
        {"Especie": "Perro", "MCV (fL)": "61.5 - 67.0", "MCH (pg)": "22.5 - 26.8", "MCHC (g/dL)": "32.0 - 36.0"},
        {"Especie": "Gato", "MCV (fL)": "39.5 - 46.5", "MCH (pg)": "13.0 - 17.5", "MCHC (g/dL)": "30.0 - 36.0"},
        {"Especie": "Oveja", "MCV (fL)": "28.5 - 32.0", "MCH (pg)": "10.8 - 12.0", "MCHC (g/dL)": "31.0 - 35.0"},
        {"Especie": "Vaca", "MCV (fL)": "40.0 - 60.0", "MCH (pg)": "14.0 - 24.0", "MCHC (g/dL)": "30.0 - 36.0"}
    ])
    st.dataframe(df_ref, use_container_width=True, hide_index=True)

    st.subheader("Detalle de pacientes por clasificación morfológica")
    filtro_tipo = st.selectbox(
        "Filtrar por tipo de anemia:",
        options=["Todos"] + tipos
    )

    df_tabla = df_anemia if filtro_tipo == "Todos" else df_anemia[df_anemia["tipo_anemia"] == filtro_tipo]

    columnas_tabla = [
        "ID muestra", "Nombre", "fecha", "especie", "sexo",
        "grupo_etario", "MCV (fL)", "MCH (pg)", "RDW-CV (%)",
        "tipo_anemia", "cromia"
    ]
    st.dataframe(df_tabla[columnas_tabla], use_container_width=True, hide_index=True)
