import streamlit as st


def render() -> None:
    st.header("Para iniciar carga tu dataset")
    st.markdown(
    '<a href="https://github.com/joe0zf/dash_hemogramas/tree/main/data" target="_blank" rel="noopener noreferrer">'
    'Puedes descargar un ejemplo aquí'
    '</a>',
    unsafe_allow_html=True,
)
