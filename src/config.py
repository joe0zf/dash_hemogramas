from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = BASE_DIR / "data" / "hemogramas_clean.csv"

APP_TITLE = "Sistema de Análisis de Datos"
APP_LAYOUT = "wide"
ALLOWED_EXTENSIONS = ["csv", "xlsx"]
MAX_FILE_SIZE = 50
DEFAULT_ROWS = 10
MAX_COLUMNS = 50

ACENTO = "#C0392B"   # rojo: anemia
GRIS   = "#CFD2D6"   # gris: datos auxiliares