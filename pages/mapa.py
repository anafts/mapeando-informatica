import streamlit as st
import folium

from streamlit_folium import st_folium

from utils.data_handler import cargar_y_limpiar_cronograma, cargar_geojson
from utils.accessibility import get_perfil_styles, PERFILES_ACCESIBILIDAD

df_cronograma = cargar_y_limpiar_cronograma()
geojson_data = cargar_geojson()

if df_cronograma is None or geojson_data is None:
    st.error("Error al cargar los archivos de datos.")
    st.stop()

st.sidebar.header("Configuración Visual")
st.sidebar.write("Seleccione el modo de contraste adecuado:")

modo_visual = st.sidebar.radio(
    "Perfil de Accesibilidad:", 
    options=list(PERFILES_ACCESIBILIDAD.keys()),
    label_visibility="collapsed"
)

estilos = get_perfil_styles(modo_visual)

st.markdown(f"""
    <style>
        p, .stMarkdown p, .stMarkdown li, label, div[data-baseweb="select"] {{
            font-size: {estilos["font_size"]}px !important;
        }}
        h2, h3 {{
            font-size: {estilos["font_size"] + 4}px !important;
        }}
    </style>
""", unsafe_allow_html=True)

st.title("Mapa de Ocupación de Aulas")

col_mapa, col_painel = st.columns([2.5, 1.2], gap="large")

with col_painel:
    st.subheader("Filtros de Búsqueda")
    
    col_dia, col_hora = st.columns(2)
    dias_mapeo = {"Lunes": 0, "Martes": 1, "Miércoles": 2, "Jueves": 3, "Viernes": 4, "Sábado": 5}
    
    with col_dia:
        dia_seleccionado = st.selectbox("Día:", options=list(dias_mapeo.keys()))
    with col_hora:
        hora_seleccionada = st.selectbox("Turno:", options=["08:00", "10:30", "13:00", "14:00", "16:00", "17:00", "18:30", "19:00"])

    clases_activas = df_cronograma[
        (df_cronograma['dia_num'] == dias_mapeo[dia_seleccionado]) & 
        (hora_seleccionada >= df_cronograma['hora_inicio']) & 
        (hora_seleccionada < df_cronograma['hora_fin'])
    ]

    st.markdown("---")
    st.subheader("Información del Aula")
    info_placeholder = st.empty()

with col_mapa:
    mapa = folium.Map(location=[-34.9032, -57.9378], zoom_start=19, max_zoom=22)
    
    folium.raster_layers.TileLayer(
        tiles="https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{y}.png",
        attr="Instituto Geográfico Nacional (IGN) - República Argentina",
        name="Argenmap (IGN)",
        overlay=False,
        control=True,
        tms=True
    ).add_to(mapa)
    
    def estilo_feature(feature):
        aula_geo = feature['properties'].get('aula')
        if not aula_geo:
            return {'fillColor': '#cbd5e1', 'color': '#94a3b8', 'weight': 1, 'fillOpacity': 0.4}
        
        aula_norm = str(aula_geo).lower().strip().replace(" ", "").replace("_", "").replace("-", "")
        esta_ocupada = aula_norm in clases_activas['aula_norm'].values
        return {
            'fillColor': estilos["color_ocupado"] if esta_ocupada else estilos["color_libre"],
            'color': 'white', 'weight': 2, 'fillOpacity': 0.6
        }

    tooltip_style = f"font-size: {estilos['font_size']}px; font-weight: bold;"

    folium.GeoJson(
        geojson_data, 
        style_function=estilo_feature, 
        tooltip=folium.GeoJsonTooltip(fields=['Nam', 'aula'])
    ).add_to(mapa)
    
    datos_mapa_clicado = st_folium(mapa, width=None, height=500, key="mapa_unlp")

    


with info_placeholder.container():
    aula_seleccionada_mapa = None
    if datos_mapa_clicado and datos_mapa_clicado.get("last_active_drawing"):
        properties = datos_mapa_clicado["last_active_drawing"].get("properties", {})
        aula_seleccionada_mapa = properties.get("aula")
        nombre_aula = properties.get("Nam", aula_seleccionada_mapa)
    
    if aula_seleccionada_mapa:
        st.info(f"**Aula Seleccionada:** {nombre_aula}")
        aula_norm_click = str(aula_seleccionada_mapa).lower().strip().replace(" ", "").replace("_", "").replace("-", "")
        info_clase = clases_activas[clases_activas['aula_norm'] == aula_norm_click]
        
        if not info_clase.empty:
            clase = info_clase.iloc[0]
            st.markdown(f"""
            * **Estado:** Ocupada
            * **Materia:** {clase['materia']}
            * **Docente:** {clase['docente']}
            * **Horario:** {clase['hora_inicio']} a {clase['hora_fin']} hs
            * **Tipo:** {clase['tipo']}
            """)
        else:
            st.success("🟢 **Estado:** Disponible / Libre.")
    else:
        st.write("Toca cualquier aula en el mapa para ver su cronograma.")