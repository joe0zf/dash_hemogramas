import streamlit as st

st.set_page_config(
    page_title="Dashboard de Emogramas en Animales",
    page_icon="📊",
    layout="wide"
)

st.title("Dashboard de Emogramas en Animales")
st.write("Bienvenido al dashboard de emogramas en animales.")

st.sidebar.title("Menú principal")
opcion = st.sidebar.selectbox(
    "Seleccione una opción",
    ["Inicio", "Cargar datos", "Análisis", "Informacion", "Sobre nosotros"]
)

if opcion == "Inicio":
    st.header("Página de inicio")
    st.success("Aplicación funcionando correctamente.")

elif opcion == "Cargar datos":
    st.header("Carga de archivos")

    archivo = st.file_uploader(
        "Seleccione un archivo CSV",
        type=["csv"]
    )

    if archivo is not None:
        import pandas as pd

        df = pd.read_csv(archivo)
        st.dataframe(df)

elif opcion == "Análisis":
    st.header("Análisis de datos")
    st.info("Próximamente implementaremos esta sección.")