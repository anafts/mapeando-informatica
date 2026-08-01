import streamlit as st

st.set_page_config(page_title="Mapa Interactivo UNLP", layout="wide")

mapa_page = st.Page(
    page="pages/mapa.py", 
    title="Mapa Interactivo", 
    icon="🗺️", 
    default=True
)

pg = st.navigation([mapa_page])
pg.run()