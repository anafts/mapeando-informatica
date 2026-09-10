import streamlit as st

st.set_page_config(
    page_title="Mapeando Informática", 
    page_icon="📍", 
    layout="centered"
)

st.title("Mapeando Informática 📍")
st.markdown("### Mapa interactivo e inclusivo de la UNLP")

st.write("""
Bienvenido a la plataforma de consulta de espacios de la Facultad de Informática. 
Este proyecto fue diseñado con un enfoque principal en la **accesibilidad universal**, 
permitiendo a los estudiantes consultar la ocupación de aulas mediante navegación visual o por teclado.

**Usá el menú lateral para navegar a la herramienta del Mapa.**
""")

with st.expander("🛠️ Sobre la tecnología"):
    st.markdown("""
    - **Data:** Extracción y limpieza con Python y Pandas.
    - **Frontend:** Streamlit con componentes accesibles.
    - **Cartografía:** GeoJSON integrado vía Folium.
    """)


    