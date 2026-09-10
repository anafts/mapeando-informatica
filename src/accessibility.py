import plotly.express as px

PERFILES_ACCESIBILIDAD = {
    "Estandard": {
        "color_ocupado": "#ef4444",
        "color_libre": "#22c55e",
        "escala_plotly": px.colors.sequential.Plasma,
        "font_size": 13,
        "template_grafico": "plotly_white"
    },
    "Protanomalía": {
        "color_ocupado": "#D55E00",
        "color_libre": "#56B4E9",
        "escala_plotly": px.colors.sequential.Viridis,
        "font_size": 13,
        "template_grafico": "plotly_white"
    },
    "Protanopia": {
        "color_ocupado": "#D55E00",
        "color_libre": "#0072B2",
        "escala_plotly": px.colors.sequential.Viridis,
        "font_size": 13,
        "template_grafico": "plotly_white"
    },
    "Deuteranopia": {
        "color_ocupado": "#D55E00",
        "color_libre": "#56B4E9",
        "escala_plotly": px.colors.sequential.Viridis,
        "font_size": 13,
        "template_grafico": "plotly_white"
    },
    "Tritanopia": {
        "color_ocupado": "#CC79A7",
        "color_libre": "#0072B2",
        "escala_plotly": px.colors.sequential.Viridis,
        "font_size": 13,
        "template_grafico": "plotly_white"
    }
}

def get_perfil_styles(modo_visual):
    return PERFILES_ACCESIBILIDAD.get(modo_visual, PERFILES_ACCESIBILIDAD["Estandard"])