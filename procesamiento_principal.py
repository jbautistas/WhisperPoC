# procesamiento_principal_modificado.py

import os
import time
import whisper
import torch
import pandas as pd
import soundfile as sf
from jiwer import wer, cer

audio_dir = 'audios/'
text_dir = 'textos/'
resultados_dir = 'resultados/'
transcripciones_dir = 'transcripciones/'

os.makedirs(resultados_dir, exist_ok=True)
os.makedirs(transcripciones_dir, exist_ok=True)

modelos = ['tiny', 'base', 'small', 'medium', 'large']

devices = ['cpu']
if torch.cuda.is_available():
    devices.append('cuda')

archivos_audio = [f for f in os.listdir(
    audio_dir) if f.endswith(('.WAV', '.MP3', '.wav', '.mp3'))]

resultados = pd.DataFrame(columns=['modelo', 'archivo_audio',
                          'device', 'time_taken', 'audio_duration', 'RTF', 'WER', 'CER'])

for device in devices:
    for modelo_nombre in modelos:
        print(
            f"Procesando con el modelo {modelo_nombre} en dispositivo {device}...")
        modelo = whisper.load_model(modelo_nombre, device=device)

        modelo_transcripciones_dir = os.path.join(
            transcripciones_dir, f"{modelo_nombre}_{device}")
        os.makedirs(modelo_transcripciones_dir, exist_ok=True)

        for archivo_audio in archivos_audio:
            ruta_audio = os.path.join(audio_dir, archivo_audio)

            with sf.SoundFile(ruta_audio) as f:
                audio_duration = len(f) / f.samplerate

            start_time = time.time()

            resultado = modelo.transcribe(ruta_audio, language='es')

            end_time = time.time()

            time_taken = end_time - start_time
            RTF = time_taken / audio_duration

            texto_transcrito = resultado['text'].strip()

            nombre_transcripcion = os.path.splitext(archivo_audio)[0] + '.txt'
            ruta_transcripcion = os.path.join(
                modelo_transcripciones_dir, nombre_transcripcion)
            with open(ruta_transcripcion, 'w', encoding='utf-8') as f:
                f.write(texto_transcrito)

            nombre_texto = os.path.splitext(archivo_audio)[0] + '.txt'
            ruta_texto = os.path.join(text_dir, nombre_texto)
            with open(ruta_texto, 'r', encoding='utf-8') as f:
                texto_referencia = f.read().strip()

            valor_wer = wer(texto_referencia, texto_transcrito)
            valor_cer = cer(texto_referencia, texto_transcrito)

            resultados = resultados._append({
                'modelo': modelo_nombre,
                'archivo_audio': archivo_audio,
                'device': device,
                'time_taken': time_taken,
                'audio_duration': audio_duration,
                'RTF': RTF,
                'WER': valor_wer,
                'CER': valor_cer
            }, ignore_index=True)

ruta_resultados = os.path.join(resultados_dir, 'metricas.csv')
resultados.to_csv(ruta_resultados, index=False)

print(
    f"Proceso completado. Los resultados se han guardado en {ruta_resultados}")
print(
    f"Las transcripciones se han guardado en el directorio '{transcripciones_dir}'")
