import requests
import json
import time
import re
from bs4 import BeautifulSoup

url_formulario = "https://gestiondocente.info.unlp.edu.ar/reservas/consulta/xaula"
url_data = "https://gestiondocente.info.unlp.edu.ar/reservas/consulta/xaula/data"

headers_html = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
}

headers_json = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest"
}

params_base = {
    "reservas_consultaxaula[periodo][from]": "09/03/2026",
    "reservas_consultaxaula[periodo][to]": "08/08/2026"
}

DIAS_MAP = {
    0: "Lunes", 1: "Martes", 2: "Miércoles", 
    3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"
}

def limpiar_nombre_archivo(nombre):
    """Reemplaza espacios y caracteres raros para crear nombres de archivo seguros."""
    nombre_limpio = nombre.replace(" ", "_")
    return re.sub(r'(?u)[^-\w.]', '', nombre_limpio)

def obtener_aulas_reales():
    """Descubre las aulas e IDs oficiales directamente desde el sistema."""
    print("Conectando con Gestión Docente para escanear las aulas oficiales...")
    try:
        response = requests.get(url_formulario, headers=headers_html)
        if response.status_code != 200:
            print(f"Error al acceder al sitio: {response.status_code}")
            return {}
        
        soup = BeautifulSoup(response.text, 'html.parser')
        select_aula = soup.find('select', {'id': 'reservas_consultaxaula_aula'}) or soup.find('select', name=lambda x: x and 'aula' in x)
        
        if not select_aula:
            print("No se encontró el menú desplegable de aulas.")
            return {}
            
        aulas = {}
        for option in select_aula.find_all('option'):
            id_val = option.get('value')
            nombre_txt = option.text.strip()
            if id_val and id_val.isdigit():
                aulas[id_val] = nombre_txt
        return aulas
    except Exception as e:
        print(f"Error escaneando formulario: {e}")
        return {}

# --- Ejecución Principal ---
diccionario_aulas = obtener_aulas_reales()

if not diccionario_aulas:
    print("No se pudo obtener el mapa de aulas. Abortando.")
    exit()

print(f"Se detectaron {len(diccionario_aulas)} aulas en el sistema de la UNLP.\n")

for id_interno, nombre_aula in diccionario_aulas.items():
    print(f"Extrayendo datos de: {nombre_aula} (ID: {id_interno})...")
    
    params = params_base.copy()
    params["reservas_consultaxaula[aula]"] = id_interno
    
    try:
        response = requests.get(url_data, headers=headers_json, params=params)
        
        if response.status_code == 200:
            reservas = response.json()
            cronograma_aula = []
            registros_unicos = set()
            
            for r in reservas:
                if not r.get("confirmada"):
                    continue
                
                materia = r.get("titulo")
                dia_num = r.get("dia")
                dia_texto = DIAS_MAP.get(dia_num, f"Desconocido ({dia_num})")
                
                h_ini = r.get("horaInicio", {})
                h_fin = r.get("horaFin", {})
                inicio_str = f"{str(h_ini.get('h', '00')).zfill(2)}:{str(h_ini.get('m', '00')).zfill(2)}"
                fin_str = f"{str(h_fin.get('h', '00')).zfill(2)}:{str(h_fin.get('m', '00')).zfill(2)}"
                
                docente_data = r.get("docente") or {}
                docente = f"{docente_data.get('apellido', '')}, {docente_data.get('nombre', '')}".strip(", ")
                tipo = r.get("tipo", "No especificado")
                
                # Control de duplicados locales por aula
                id_unico = (materia, dia_num, inicio_str, fin_str)
                
                if id_unico not in registros_unicos:
                    registros_unicos.add(id_unico)
                    cronograma_aula.append({
                        "materia": materia,
                        "tipo": tipo,
                        "dia": dia_texto,
                        "dia_num": dia_num,
                        "hora_inicio": inicio_str,
                        "hora_fin": fin_str,
                        "docente": docente if docente else "No asignado",
                        "semestre": r.get("semestre")
                    })
            
            # Guardar el JSON específico de ESTA aula
            nombre_archivo = f"{limpiar_nombre_archivo(nombre_aula)}.json"
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                json.dump(cronograma_aula, f, ensure_ascii=False, indent=4)
                
            print(f"-> Guardado exitosamente en '{nombre_archivo}' con {len(cronograma_aula)} clases.")
            
        else:
            print(f"-> Error del servidor ({response.status_code}) para {nombre_aula}")
            
    except Exception as e:
        print(f"-> Error inesperado en {nombre_aula}: {e}")
        
    time.sleep(0.6) # Delay de cortesía

print("\n¡Todo listo! Tenés un archivo JSON por cada aula en tu directorio.")