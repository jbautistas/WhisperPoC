import os
import unicodedata
import re


def normalizar_texto(texto):
    texto = texto.lower()
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    texto = re.sub(r'[^\w\s]', '', texto)
    texto = re.sub(r'\d+', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto


directorio_origen = 'textos_no_normalizados'
directorio_destino = 'textos'

if not os.path.exists(directorio_destino):
    os.makedirs(directorio_destino)

for nombre_archivo in os.listdir(directorio_origen):
    ruta_archivo_origen = os.path.join(directorio_origen, nombre_archivo)
    if os.path.isfile(ruta_archivo_origen) and nombre_archivo.endswith('.txt'):
        with open(ruta_archivo_origen, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        contenido_normalizado = normalizar_texto(contenido)
        ruta_archivo_destino = os.path.join(directorio_destino, nombre_archivo)
        with open(ruta_archivo_destino, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido_normalizado)
        print(
            f'Archivo "{nombre_archivo}" procesado y guardado en "{directorio_destino}".')
