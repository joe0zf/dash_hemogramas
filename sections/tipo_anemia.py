import streamlit as st


def render() -> None:
    st.header("Análisis de datos")
    datos = st.session_state.get("dataset")

    if datos is None:
        st.info("Primero cargue un archivo CSV en la sección Cargar datos.")
        return

    st.write(f"El conjunto de datos contiene {len(datos)} registros.")
