import os
import json
import csv

# Nombre del archivo CSV de salida
archivo_csv_salida = "cronograma_unificado.csv"

# Buscar todos los archivos .json en el directorio actual
archivos_json = [f for f in os.listdir('.') if f.endswith('.json')]

if not archivos_json:
    print("No se encontraron archivos JSON en esta carpeta. Asegurate de correr el script donde se guardaron.")
    exit()

# Definir las cabeceras del CSV basadas en tu estructura
cabeceras = ["aula_codigo", "materia", "tipo", "dia", "dia_num", "hora_inicio", "hora_fin", "docente", "semestre"]

print(f"Procesando {len(archivos_json)} archivos JSON...")

with open(archivo_csv_salida, mode='w', newline='', encoding='utf-8') as archivo_csv:
    escritor = csv.DictWriter(archivo_csv, fieldnames=cabeceras)
    escritor.writeheader()  # Escribimos los nombres de las columnas
    
    contador_filas = 0
    
    for archivo in archivos_json:
        # Deducimos el nombre del aula limpiando la extensión (ej: "Aula_Android.json" -> "Aula_Android")
        nombre_aula = archivo.replace(".json", "")
        
        with open(archivo, mode='r', encoding='utf-8') as f:
            try:
                clases = json.load(f)
                
                for clase in clases:
                    # Construimos la fila para el CSV inyectando el código del aula
                    fila = {
                        "aula_codigo": nombre_aula,
                        "materia": clase.get("materia"),
                        "tipo": clase.get("tipo"),
                        "dia": clase.get("dia"),
                        "dia_num": clase.get("dia_num"),
                        "hora_inicio": clase.get("hora_inicio"),
                        "hora_fin": clase.get("hora_fin"),
                        "docente": clase.get("docente"),
                        "semestre": clase.get("semestre")
                    }
                    escritor.writerow(fila)
                    contador_filas += 1
                    
            except json.JSONDecodeError:
                print(f"-> Error al leer el archivo {archivo}, saltando...")

print(f"¡Listo! Se creó '{archivo_csv_salida}' con {contador_filas} registros en total.")