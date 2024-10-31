# WhisperPoC

# Benchmark de Reconocimiento de Voz con Modelos Whisper

Este repositorio contiene scripts para realizar un benchmark de los modelos Whisper de OpenAI en tareas de reconocimiento de voz, comparando el rendimiento entre la ejecución en CPU y GPU. Los scripts procesan archivos de audio, los transcriben utilizando diferentes modelos Whisper, calculan métricas de error (WER y CER), registran los tiempos de ejecución y generan gráficos comparativos.

### Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Estructura de Carpetas](#estructura-de-carpetas)
- [Preparación de Datos](#preparación-de-datos)
- [Uso](#uso)
  - [1. Preprocesamiento de Textos](#1-preprocesamiento-de-textos)
  - [2. Procesamiento Principal](#2-procesamiento-principal)
  - [3. Generación de Gráficos](#3-generación-de-gráficos)
- [Descripción de los Scripts](#descripción-de-los-scripts)
- [Resultados](#resultados)
- [Licencia](#licencia)

---

## Requisitos Previos

- Python 3.8 o superior
- Una GPU NVIDIA con soporte CUDA (opcional, para ejecución en GPU)
- Git (para clonar el repositorio)
- **FFmpeg** instalado en tu sistema (requerido para el procesamiento de audio)
- **PyTorch 1.10 o superior** (requerido por Whisper)

## Instalación

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/jbautistas/WhisperPoC.git
   cd WhisperPoC

2. **Instala FFmpeg:**

   - **Windows:**

     - Descarga FFmpeg desde el [sitio oficial](https://ffmpeg.org/download.html).
     - Extrae los archivos y agrega la carpeta `bin` a la variable de entorno PATH de tu sistema.

   - **Linux (Debian/Ubuntu):**

     ```bash
     sudo apt update
     sudo apt install ffmpeg
     ```

   - **macOS:**

     ```bash
     brew install ffmpeg
     ```

3. **Crea un entorno virtual (recomendado):**

   ```bash
   python -m venv venv
   ```

4. **Activa el entorno virtual:**

   - En Windows:

     ```bash
     venv\Scripts\activate
     ```

   - En Linux/Mac:

     ```bash
     source venv/bin/activate
     ```

5. **Instala PyTorch:**

   Visita la página de [Inicio Rápido de PyTorch](https://pytorch.org/get-started/locally/) para encontrar el comando de instalación adecuado para tu sistema.

   - **Solo CPU:**

     ```bash
     pip install torch torchvision torchaudio
     ```

   - **GPU con CUDA:**

     Reemplaza `<VERSION_CUDA>` con tu versión de CUDA (por ejemplo, `cu118` para CUDA 11.8):

     ```bash
     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/<VERSION_CUDA>
     ```

     Ejemplo para CUDA 11.8:

     ```bash
     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
     ```

6. **Instala los paquetes Python requeridos:**

   ```bash
   pip install -r requirements.txt
   ```

   Esto instalará todos los paquetes necesarios, incluyendo `openai-whisper`, `pandas`, `jiwer`, `matplotlib`, `seaborn` y `soundfile`.

## Estructura de Carpetas

El proyecto espera la siguiente estructura de carpetas:

```
├── audios/
│   ├── audio1.wav
│   ├── audio2.wav
│   └── ...
├── textos_no_normalizados/
│   ├── audio1.txt
│   ├── audio2.txt
│   └── ...
├── textos/
│   └── (generado después del preprocesamiento)
├── resultados/
│   └── (generado después del procesamiento principal)
├── transcripciones/
│   └── (generado después del procesamiento principal)
├── preprocesamiento_textos.py
├── procesamiento_principal.py
├── graficos.py
├── requirements.txt
└── README.md
```

- **audios/**: Carpeta que contiene los archivos de audio (`.wav` o `.mp3`) a transcribir.
- **textos_no_normalizados/**: Carpeta que contiene las transcripciones de referencia correspondientes a cada archivo de audio, **sin normalizar**.
- **textos/**: Carpeta donde se guardarán los textos normalizados después del preprocesamiento.
- **resultados/**: Carpeta donde se guardarán los resultados y métricas después del procesamiento principal.
- **transcripciones/**: Carpeta donde se guardarán las transcripciones generadas por los modelos.

## Preparación de Datos

1. **Coloca tus archivos de audio en la carpeta `audios/`.**

   - Formatos soportados: `.wav`, `.mp3`
   - Asegúrate de que los nombres de los archivos de audio no contengan espacios y coincidan con los nombres de los textos.

2. **Coloca las transcripciones de referencia correspondientes en la carpeta `textos_no_normalizados/`.**

   - Formato de archivo: Archivos de texto plano (`.txt`)
   - El nombre del archivo de transcripción debe coincidir con el del audio correspondiente. Por ejemplo, `audio1.wav` y `audio1.txt`.

## Uso

### 1. Preprocesamiento de Textos

Normaliza las transcripciones de texto para eliminar acentos, puntuación, números y espacios adicionales.

Ejecuta el siguiente comando:

```bash
python preprocesamiento_textos.py
```

Este script leerá los archivos de texto desde `textos_no_normalizados/`, normalizará el contenido y guardará los textos normalizados en la carpeta `textos/`.

### 2. Procesamiento Principal

Ejecuta el proceso de transcripción utilizando diferentes modelos Whisper tanto en CPU como en GPU, registra los tiempos de ejecución y calcula las métricas de error.

Ejecuta el siguiente comando:

```bash
python procesamiento_principal.py
```

Este script:

- Carga cada modelo Whisper (`tiny`, `base`, `small`, `medium`, `large`).
- Para cada modelo, procesa cada archivo de audio en `audios/` en ambos dispositivos (si están disponibles).
- Transcribe los archivos de audio y guarda las transcripciones en `transcripciones/`.
- Calcula la Tasa de Error de Palabra (WER) y la Tasa de Error de Caracter (CER) comparando con las transcripciones de referencia en `textos/`.
- Registra el tiempo de ejecución y calcula el Factor de Tiempo Real (RTF) para cada transcripción.
- Guarda todas las métricas en un archivo CSV `resultados/metricas.csv`.

**Nota:**

- Si solo tienes CPU disponible, el script omitirá automáticamente la ejecución en GPU.
- Procesar con modelos más grandes (por ejemplo, `large`) puede requerir una cantidad significativa de memoria. Asegúrate de que tu sistema tenga suficiente RAM, el modelo más grande estima unos 10 GB de RAM.

### 3. Generación de Gráficos

Genera gráficos comparativos basados en los resultados.

Ejecuta el siguiente comando:

```bash
python graficos.py
```

Este script leerá las métricas desde `resultados/metricas.csv` y generará gráficos comparando:

- WER y CER entre diferentes modelos.
- Tiempos de ejecución y RTF entre CPU y GPU.
- Factores de aceleración entre CPU y GPU.

Los gráficos se guardarán como archivos PNG en el directorio actual.

## Descripción de los Scripts

### preprocesamiento_textos.py

Este script normaliza las transcripciones de texto:

- Convierte el texto a minúsculas.
- Elimina acentos y diacríticos.
- Elimina puntuación y números.
- Elimina espacios adicionales.

**Uso:**

```bash
python preprocesamiento_textos.py
```

### procesamiento_principal.py

Este es el script principal de procesamiento que:

- Carga los modelos Whisper.
- Transcribe archivos de audio en ambos dispositivos (CPU y GPU).
- Registra los tiempos de ejecución y calcula el RTF.
- Calcula las métricas WER y CER.
- Guarda los resultados en un archivo CSV.

**Uso:**

```bash
python procesamiento_principal.py
```

### graficos.py

Este script genera gráficos comparativos basados en las métricas recopiladas.

- Genera gráficos de barras para WER y CER promedio por modelo.
- Genera gráficos de barras para tiempo de ejecución promedio y RTF por modelo y dispositivo.
- Calcula y grafica factores de aceleración entre CPU y GPU.
- Genera gráficos de líneas y cajas para análisis detallado.

**Uso:**

```bash
python graficos.py
```

## Resultados

Después de ejecutar los scripts, encontrarás:

- **Transcripciones** en `transcripciones/`, organizadas por modelo y dispositivo.
- **Archivo CSV de métricas** en `resultados/metricas.csv`, que contiene resultados detallados.
- **Gráficos** en el directorio actual, mostrando análisis comparativos.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.
