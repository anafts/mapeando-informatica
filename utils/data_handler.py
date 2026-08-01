import json

import pandas as pd
import streamlit as st

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent 
CRONOGRAMA_PATH = BASE_DIR / "data" / "cronograma_unificado.json"
GEOJSON_PATH = BASE_DIR / "data" / "aulas.geojson"

@st.cache_data 
def cargar_y_limpiar_cronograma():
    try:
        df = pd.read_json(CRONOGRAMA_PATH)
        df['materia'] = df['materia'].fillna('Sala Libre / Sin Actividad').astype(str)
        df['docente'] = df['docente'].fillna('No asignado').astype(str)
        df['tipo'] = df['tipo'].fillna('General').astype(str)
        
        if 'aula' in df.columns and 'aula_codigo' not in df.columns:
            df['aula_codigo'] = df['aula']
            
        df['aula_norm'] = df['aula_codigo'].astype(str).str.lower().str.strip().str.replace(r'[\s_-]', '', regex=True)
        return df
    except Exception as e:
        return None

def cargar_geojson():
    with open(GEOJSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)