import pandas as pd
import streamlit as st


def render_sidebar() -> None:
    st.subheader("Cargar datos")
    archivo = st.file_uploader(
        "Seleccione un archivo CSV",
        type=["csv"],
        key="dataset_upload",
    )

    if archivo is not None:
        datos = pd.read_csv(archivo)
        st.session_state["dataset"] = datos
        st.caption(f"Archivo cargado: {archivo.name}")
        return datos


def render() -> None:
    st.header("Carga de archivos")
    datos = st.session_state.get("dataset")

    if datos is None:
        st.info("Cargue un archivo CSV desde la parte superior de la barra lateral.")
    else:
        st.dataframe(datos)
