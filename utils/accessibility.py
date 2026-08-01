import plotly.express as px

PERFILES_ACCESIBILIDAD = {
    "Estandard": {
        "color_ocupado": "#ef4444",
        "color_libre": "#22c55e",
        "escala_plotly": px.colors.sequential.Plasma,
        "font_size": 13,
        "template_grafico": "plotly_white"
    },
    "Daltonismo": {
        "color_ocupado": "#d55e00", 
        "color_libre": "#56b4e9",  
        "escala_plotly": px.colors.sequential.Viridis,
        "font_size": 13,
        "template_grafico": "plotly_white"
    },
    "Baja Visión": {  
        "color_ocupado": "#ff0000",
        "color_libre": "#00ff00",
        "escala_plotly": ["#ffffff", "#000000"],
        "font_size": 18,
        "template_grafico": "plotly_dark"
    }
}

def get_perfil_styles(modo_visual):
    return PERFILES_ACCESIBILIDAD.get(modo_visual, PERFILES_ACCESIBILIDAD["Estandard"])