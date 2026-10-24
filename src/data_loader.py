import pandas as pd

from .config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE
def load_data(file):
    if file is None:
        return None
    extension = file.name.rsplit(".", 1)[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Tipo de archivo no permitido. Solo se permiten archivos: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    if file.size > MAX_FILE_SIZE * 1024 * 1024:
        raise ValueError("El archivo supera el tamaño permitido.")

    file.seek(0)

    if extension == "csv":
        try:
            df = pd.read_csv(file)
        except UnicodeDecodeError:
            file.seek(0)
            df = pd.read_csv(file, encoding="latin-1")

    elif extension == "xlsx":
        df = pd.read_excel(file)

    return df


def get_info(df):

    info = {
        "filas": df.shape[0],
        "columnas": df.shape[1],
        "duplicados": int(df.duplicated().sum()),
        "valores_nulos": int(df.isnull().sum().sum()),
        "nombres_columnas": df.columns.tolist()
    }

    return info