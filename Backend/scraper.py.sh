# Crear un directorio para el scraper y entrar
mkdir scraper_unlp && cd scraper_unlp

# Crear un entorno virtual de Python
python -m venv venv

# Activar el entorno virtual
source venv/bin/activate

# Instalar las librerías necesarias
pip install requests beautifulsoup4