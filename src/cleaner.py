import json
import pandas as pd
from pathlib import Path

from src.config import RAW_SCHEDULE_PATH, PROCESSED_SCHEDULE_PATH

def load_raw_data(file):
    """Loads the raw JSON data scraped from the faculty website."""
    with open(file, 'r', encoding='utf-8') as f: 
        data = json.load(f) 
    return pd.DataFrame(data)

def clean_schedule_data(df):
    """Cleans and standardizes the DataFrame."""
    try:
        df['materia'] = df['materia'].fillna('Sala Libre / Sin Actividad').astype(str)
        df['docente'] = df['docente'].fillna('No asignado').astype(str)
        df['tipo'] = df['tipo'].fillna('General').astype(str)

        if 'aula' in df.columns and 'aula_codigo' not in df.columns:
            df['aula_codigo'] = df['aula'] 

        df['aula_norm'] = (
            df['aula_codigo']
            .astype(str)
            .str.lower()
            .str.strip()
            .str.replace(r'[\s_-]', '', regex=True)
        )

        df = df.drop_duplicates()
        return df

    except Exception as e:
        print(f"Error during cleaning: {e}")
        return pd.DataFrame() 


def export_clean_data(df: pd.DataFrame, output_path: Path) -> None:
    """Exports the cleaned DataFrame to a new JSON file."""
    if not df.empty:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_json(output_path, orient='records', force_ascii=False, indent=4)
    else:
        print("Warning: DataFrame is empty. Export aborted.")


if __name__ == "__main__":
    print(f"Buscando archivo en: {RAW_SCHEDULE_PATH.resolve()}")
    
    if not RAW_SCHEDULE_PATH.exists():
        print("ERROR: El archivo cronograma_unificado.json NO existe en esa ruta.")
    else:
        print("Archivo encontrado. Leyendo y limpiando...")
        raw_df = load_raw_data(RAW_SCHEDULE_PATH)
        print(f"Filas originales leídas: {len(raw_df)}")
        
        clean_df = clean_schedule_data(raw_df)
        print(f"Filas después de limpiar: {len(clean_df)}")
        
        export_clean_data(clean_df, PROCESSED_SCHEDULE_PATH)