# Análisis de Relaciones de Personajes en "Marmalade Boy"

Este repositorio contiene un análisis detallado de las relaciones entre los personajes de "Marmalade Boy" utilizando técnicas de procesamiento de texto y visualización de datos en Python. El análisis incluye la frecuencia de diálogos, la co-ocurrencia de personajes en escenas y una visualización de las relaciones entre personajes.

## Contenido

- `main.py`: Script principal que realiza el análisis.
- `script.csv`: Archivo CSV con el guion de "Marmalade Boy" (diálogos de los personajes).
- `README.md`: Este archivo de documentación.

## Requisitos

El script se ha desarrollado con las siguientes librerías y versiones:

- `numpy`
- `pandas`
- `matplotlib`
- `plotly`
- `seaborn`
- `PIL` (Pillow)
- `nltk`
- `scikit-learn`
- `networkx`

Puedes instalar todas las dependencias necesarias usando `pip`:

```bash
pip install numpy pandas matplotlib plotly seaborn pillow nltk scikit-learn networkx
```

# Uso
## Preparar el Entorno:

Clona este repositorio en tu máquina local.
Asegúrate de tener las librerías necesarias instaladas.
## Datos:

Asegúrate de mover el archivo CSV a la nueva carpeta `data/` y actualizar el script `script.py` para que lea el archivo desde esta nueva ubicación.
## Ejecutar el Análisis:

Ejecuta el script script.py usando Python:
bash
Copiar código
python script.py
El script generará visualizaciones de los datos y análisis de texto basados en el guion.

# Descripción del Script
El script realiza las siguientes tareas:

### Carga de Datos:

Lee el archivo CSV con los diálogos de los personajes y prepara el DataFrame.
### Análisis de Frecuencia de Personajes:

Calcula y visualiza la frecuencia de aparición de cada personaje.
### Preprocesamiento de Texto:

Limpia, tokeniza y lematiza los diálogos.
Calcula la frecuencia de términos y genera una lista de las palabras más comunes.
### Análisis de Escenas y Líneas de Diálogo:

Calcula el número de escenas y líneas de diálogo por personaje.
Visualiza estos datos con gráficos de barras.
### Análisis de Relaciones entre Personajes:

Analiza las interacciones entre pares y tríos de personajes en diferentes escenas.
Visualiza las relaciones usando un gráfico de red (networkx).
## Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un problema o una solicitud de extracción (pull request) para discutir cualquier mejora o corrección.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.