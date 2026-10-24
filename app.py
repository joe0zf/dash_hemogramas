import streamlit as st

from sections import concentracion, home, prevalencia, severidad, tipo_anemia
from src import data_loader

st.set_page_config(
    page_title="Dashboard de Emogramas en Animales",
    page_icon="🩸",
    layout="wide"
)

# st.title("HemoVet - Bethoven")
# st.write("Perfil de salud hematológica de la población atendida")
# st.write("Para iniciar carga tu dataset")

with st.sidebar:
    st.header("Cargar datos")
    archivo = st.file_uploader(
        "Seleccione un archivo CSV", type=["csv", "xlsx"],
        label_visibility="collapsed",
    )
    st.divider()
    st.title("Menú principal")
    opcion = st.radio(
        "Seleccione una sección",
        ["Inicio", "Prevalencia", "Tipo de anemia", "Concentración", "Severidad"],
        label_visibility="collapsed",
    )
try:
    df = data_loader.load_dataset(archivo)
except ValueError as e:
    st.sidebar.error(str(e))
    df = data_loader.load_default()

paginas = {
    "Inicio": home.render,
    "Prevalencia": prevalencia.render,
    "Tipo de anemia": tipo_anemia.render,
    "Concentración": concentracion.render,
    "Severidad": severidad.render,
}
paginas[opcion](df)