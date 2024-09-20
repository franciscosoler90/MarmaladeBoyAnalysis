# Análisis de Relaciones de Personajes en "Marmalade Boy"

Este repositorio contiene un análisis detallado de las relaciones entre los personajes de "Marmalade Boy" utilizando técnicas de procesamiento de texto y visualización de datos en Python. El análisis incluye la frecuencia de diálogos, la co-ocurrencia de personajes en escenas y una visualización de las relaciones entre personajes.

## Tabla de Contenidos
- [Características](#características)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Tecnologías](#tecnologías)

## Contenido

- `main.py`: Script principal que realiza el análisis.
- `script.csv`: Archivo CSV con el guion de "Marmalade Boy" (diálogos de los personajes).
- `README.md`: Este archivo de documentación.

## Características
- **Conteo de Diálogos por Personaje**: Analiza el número de diálogos por personaje.
- **Desglose de Escenas**: Analiza el número de escenas y líneas habladas por personaje.
- **Gráfico de Interacciones entre Personajes**: Visualiza las interacciones entre personajes usando grafos de red.

## Instalación

### Requisitos Previos
Asegúrate de tener instalados los siguientes programas en tu sistema:
- [Python 3.7+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

### Pasos
1. **Clona el repositorio**
   ```bash
   git clone https://github.com/franciscosoler90/MarmaladeBoyAnalysis.git
   cd MarmaladeBoyAnalysis
   ```

2. **Crea un entorno virtual (opcional, pero recomendado)**
```bash
python -m venv env
source env/bin/activate   # En Windows: env\Scripts\activate
```

1. **Instala las dependencias necesarias**
```bash
pip install -r requirements.txt
```

1. **Descarga los corpus de NLTK** El proyecto requiere las stopwords y wordnet de NLTK. Ejecuta los siguientes comandos para descargarlos:

```bash
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

## Uso
1. Coloca el guion de Marmalade Boy en el archivo data/script.csv. El formato debe incluir columnas como:

- `index`: El número de línea en el guion.
- `episode`: Número de episodio.
- `scene`: Número de escena.
- `character`: Nombre del personaje.
- `dialogue`: El diálogo hablado por el personaje.

1. Ejecuta el script main.py para iniciar el análisis:

```bash
python main.py
```
1. El programa generará:

- Gráficos de barras con el conteo de diálogos por personaje.
- Distribución de líneas por escena y personaje.
- Un gráfico de red de las interacciones entre personajes.

### Estructura del Proyecto

```bash
marmalade-boy-analysis/
│
├── data/
│   └── script.csv                # Archivo del guion de entrada
│
├── modules/
│   ├── data_processing.py         # Funciones para cargar y procesar datos
│   ├── text_processing.py         # Limpieza y análisis de texto con NLP
│   └── visualizations.py          # Funciones para generar gráficos
│
├── main.py                        # Script principal para ejecutar el análisis
├── requirements.txt               # Dependencias del proyecto
└── README.md                      # Descripción del proyecto
```

### Tecnologías
- Python: Lenguaje de programación principal.
- Pandas: Para la manipulación de datos.
- Matplotlib y Seaborn: Para la visualización de datos.
- NLTK: Para el procesamiento de lenguaje natural.
- NetworkX: Para construir y visualizar los grafos de interacción de personajes.


## Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un problema o una solicitud de extracción (pull request) para discutir cualquier mejora o corrección.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.