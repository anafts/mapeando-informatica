import json
import folium

import pandas as pd
import streamlit as st

from streamlit_folium import st_folium
from src.config import PROCESSED_SCHEDULE_PATH, GEOJSON_PATH
from src.accessibility import get_perfil_styles, PERFILES_ACCESIBILIDAD

@st.cache_data
def load_clean_data():
    try:
        return pd.read_json(PROCESSED_SCHEDULE_PATH)
    except Exception:
        return pd.DataFrame()

@st.cache_data
def load_geojson():
    try:
        with open(GEOJSON_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

df_schedule = load_clean_data()
geojson_data = load_geojson()

if df_schedule.empty or not geojson_data:
    st.error("Error al cargar los archivos de datos. Ejecutá el pipeline de datos primero.")
    st.stop()


st.sidebar.header("Configuración Visual")
st.sidebar.write("Seleccione el modo de contraste adecuado:")

visual_mode = st.sidebar.radio(
    "Perfil de Accesibilidad:", 
    options=list(PERFILES_ACCESIBILIDAD.keys()),
    label_visibility="collapsed"
)

styles = get_perfil_styles(visual_mode)

st.markdown(f"""
    <style>
        p, .stMarkdown p, .stMarkdown li, label, div[data-baseweb="select"] {{
            font-size: {styles["font_size"]}px !important;
        }}
        h2, h3 {{
            font-size: {styles["font_size"] + 4}px !important;
        }}
    </style>
""", unsafe_allow_html=True)


st.title("Mapa de Ocupación de Aulas")

col_map, col_panel = st.columns([2.5, 1.2], gap="large")

with col_panel:
    st.subheader("Filtros de Búsqueda")
    
    col_day, col_time = st.columns(2)
    days_mapping = {"Lunes": 0, "Martes": 1, "Miércoles": 2, "Jueves": 3, "Viernes": 4, "Sábado": 5}
    
    with col_day:
        selected_day = st.selectbox("Día:", options=list(days_mapping.keys()))
    with col_time:
        selected_time = st.selectbox("Turno:", options=["08:00", "10:30", "13:00", "14:00", "16:00", "17:00", "18:30", "19:00"])

    active_classes = df_schedule[
        (df_schedule['dia_num'] == days_mapping[selected_day]) & 
        (selected_time >= df_schedule['hora_inicio']) & 
        (selected_time < df_schedule['hora_fin'])
    ]

    available_classrooms = sorted(df_schedule['aula_codigo'].dropna().unique())
    
    selected_classroom_dropdown = st.selectbox(
        "Elegí un aula (alternativa al mapa):",
        options=["-- Seleccionar --"] + list(available_classrooms),
        key="selector_aula"
    )

    st.markdown("---")
    st.subheader("Información del Aula")
    
    info_placeholder = st.empty()

with col_map:
    map_obj = folium.Map(location=[-34.9032, -57.9378], zoom_start=19, max_zoom=22)
    
    folium.raster_layers.TileLayer(
        tiles="https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{y}.png",
        attr="Instituto Geográfico Nacional (IGN) - República Argentina",
        name="Argenmap (IGN)",
        overlay=False,
        control=True,
        tms=True
    ).add_to(map_obj)
    
    def feature_style(feature):
        geo_classroom = feature['properties'].get('aula')
        if not geo_classroom:
            return {'fillColor': '#cbd5e1', 'color': '#94a3b8', 'weight': 1, 'fillOpacity': 0.4}
        
        norm_classroom = str(geo_classroom).lower().strip().replace(" ", "").replace("_", "").replace("-", "")
        is_occupied = norm_classroom in active_classes['aula_norm'].values
        return {
            'fillColor': styles["color_ocupado"] if is_occupied else styles["color_libre"],
            'color': 'white', 'weight': 2, 'fillOpacity': 0.6
        }

    folium.GeoJson(
        geojson_data, 
        style_function=feature_style, 
        tooltip=folium.GeoJsonTooltip(fields=['Nam', 'aula'])
    ).add_to(map_obj)
    
    map_click_data = st_folium(map_obj, width=None, height=500, key="mapa_unlp")


with info_placeholder.container():
    selected_classroom_map = None
    classroom_name = None

    if map_click_data and map_click_data.get("last_active_drawing"):
        properties = map_click_data["last_active_drawing"].get("properties", {})
        selected_classroom_map = properties.get("aula")
        classroom_name = properties.get("Nam", selected_classroom_map)


    selected_from_dropdown = (
        selected_classroom_dropdown 
        if selected_classroom_dropdown != "-- Seleccionar --" 
        else None
    )

    final_classroom = selected_from_dropdown or selected_classroom_map
    display_name = selected_from_dropdown if selected_from_dropdown else classroom_name

    if final_classroom:
        norm_classroom = str(final_classroom).lower().strip().replace(" ", "").replace("_", "").replace("-", "")
        class_info = active_classes[active_classes['aula_norm'] == norm_classroom]
        
        st.info(f"**Aula Seleccionada:** {display_name or final_classroom}")
        
        if not class_info.empty:
            current_class = class_info.iloc[0]
            st.markdown(f"""
            * **Estado:** Ocupada
            * **Materia:** {current_class['materia']}
            * **Docente:** {current_class['docente']}
            * **Horario:** {current_class['hora_inicio']} a {current_class['hora_fin']} hs
            * **Tipo:** {current_class['tipo']}
            """)
        else:
            st.success("🟢 **Estado:** Disponible / Libre.")
    else:
        st.write("Toca cualquier aula en el mapa o seleccionala en la lista para ver su cronograma.")