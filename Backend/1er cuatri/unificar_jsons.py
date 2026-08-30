import os
import json

# Nombre del archivo JSON unificado de salida
archivo_json_salida = "cronograma_unificado.json"

# Buscar todos los archivos .json en el directorio actual (excluyendo el de salida si ya existe)
archivos_json = [
    f for f in os.listdir('.') 
    if f.endswith('.json') and f != archivo_json_salida and f != 'package.json'
]

if not archivos_json:
    print("No se encontraron archivos JSON de aulas en esta carpeta.")
    exit()

cronograma_unificado = []
contador_clases = 0

print(f"Unificando {len(archivos_json)} archivos de aulas...")

for archivo in archivos_json:
    # El nombre del archivo se convierte en el código del aula (ej: "Aula_10-A.json" -> "Aula_10-A")
    aula_codigo = archivo.replace(".json", "")
    
    with open(archivo, mode='r', encoding='utf-8') as f:
        try:
            clases_aula = json.load(f)
            
            for clase in clases_aula:
                # Clonamos el diccionario de la clase e inyectamos el aula_codigo al principio
                clase_unificada = {"aula_codigo": aula_codigo}
                clase_unificada.update(clase)
                
                cronograma_unificado.append(clase_unificada)
                contador_clases += 1
                
        except json.JSONDecodeError:
            print(f"-> Error al decodificar el archivo: {archivo}. Saltando...")

# Guardar el array gigante con todos los datos consolidados
with open(archivo_json_salida, mode='w', encoding='utf-8') as f_salida:
    json.dump(cronograma_unificado, f_salida, ensure_ascii=False, indent=4)

print(f"\n¡Listo! Se creó '{archivo_json_salida}' con éxito.")
print(f"Se consolidaron {contador_clases} horarios de cursada en un único set de datos.")