# Mapeando Informática
Mapa interactivo e inclusivo de ocupación de aulas y espacios para la Facultad de Informática (UNLP).

## 📌 Descripción del Proyecto: 
A la hora de desarrollar este proyecto, nos pareció fundamental darle un enfoque inclusivo a la descripción y exploración de los espacios de nuestra facultad, 
ya que esto tiene un impacto directo e inmediato en nuestra comunidad.

El proyecto consiste en una aplicación web interactiva desarrollada con Streamlit que, mediante cartografía digital (incorporando capas de Argenmap - IGN), visibiliza 
y describe los sectores que habitamos diariamente en la facultad (aulas, hall, biblioteca, buffet, patio y pasillos).

## 🎯 Problemática que busca resolver:
El objetivo principal es resolver y visibilizar las barreras de accesibilidad que enfrentan los miembros de la comunidad universitaria al consultar la ocupación de aulas 
y consultar mapas, enfocándose en:

- Personas con daltonismo (mediante paletas de colores adaptadas y amigables).

- Personas con visibilidad reducida (ajuste dinámico de tamaños de texto, contrastes altos y elementos legibles).

## 💡 Desafío identificado: 
¿Es posible crear una aplicación universal para absolutamente todos? El desafío principal radica en que la diversidad funcional es muy amplia. En esta primera etapa, el prototipo contempla soluciones para daltonismo y visibilidad reducida.

## 🛠️ Tecnologías Utilizadas
- Python 3.x
- Streamlit (Interfaz interactiva y gestión de accesibilidad)
- Folium & Streamlit-Folium (Cartografía interactiva y visualización de GeoJSON / Argenmap IGN)
- Pandas (Procesamiento, limpieza y filtrado de datos del cronograma)

## 🔧 Instalación y Ejecución
Requisitos previos
Tener instalado Python 3 o superior y git.

## 🚀 Guía de Configuración e Instalación

Seguí estos pasos en tu terminal para configurar el proyecto localmente en tu computadora:

### 1. Clonar el repositorio
Descargá el proyecto en tu máquina local y accedé a la carpeta principal:

        git clone https://github.com/anafts/mapeando-informatica.git

Accedé a la carpeta principal:

        cd mapeando-informatica
### 2. Crear el entorno virtual (VENV)
Para mantener las librerías del proyecto aisladas y no interferir con tu sistema, creá un entorno virtual ejecutando:

        python -m venv .venv

### 3. Activar el entorno
Para comenzar a usar el entorno, debés activarlo. Según tu sistema operativo, utilizá el comando correspondiente:

        Windows: .venv\Scripts\activate

        Mac/Linux: source .venv/bin/activate

(Nota: Te vas a dar cuenta de que el entorno está activo porque vas a ver el prefijo (.venv) al inicio de la línea en tu terminal).

### 4. Instalar las dependencias
Con el entorno activado, procedé a instalar Streamlit, Jupyter y las demás librerías necesarias para que el proyecto funcione:

        pip install -r requirements.txt


### 5. Iniciar la aplicación Streamlit:
        
        streamlit run app.py