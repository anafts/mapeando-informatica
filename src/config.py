from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
SPATIAL_DIR = DATA_DIR / "spatial"

RAW_SCHEDULE_PATH = RAW_DIR / "cronograma_unificado.json"
PROCESSED_SCHEDULE_PATH = PROCESSED_DIR / "cronograma_limpio.json"
GEOJSON_PATH = SPATIAL_DIR / "aulas.geojson"