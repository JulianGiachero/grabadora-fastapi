
import os
import numpy as np
import sounddevice as sd
import soundfile as sf
import librosa
import glob
from fastapi import HTTPException

SAMPLE_RATE = 44100
CHANNELS = 1
GRABACIONES_DIR = "grabaciones"
os.makedirs(GRABACIONES_DIR, exist_ok=True)

def obtener_nombre_grabacion():
    contador = 1
    while True:
        nombre = f"grabacion_{contador}.wav"
        ruta = os.path.join(GRABACIONES_DIR, nombre)
        if not os.path.exists(ruta):
            return ruta
        contador += 1

def grabar_audio(segundos: int) -> str:
    nombre_archivo = obtener_nombre_grabacion()
    print(f"Grabando {segundos} segundos en {nombre_archivo}...")
    audio = sd.rec(int(segundos * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS)
    sd.wait()
    sf.write(nombre_archivo, audio, SAMPLE_RATE)
    return os.path.basename(nombre_archivo)

def listar_grabaciones():
    return sorted([f for f in os.listdir(GRABACIONES_DIR) if f.endswith(".wav")])

def eliminar_grabacion(nombre: str):
    ruta = os.path.join(GRABACIONES_DIR, nombre)
    if os.path.exists(ruta):
        os.remove(ruta)
        return True
    raise HTTPException(status_code=404, detail="Archivo no encontrado")

def renombrar_grabacion(actual: str, nuevo: str):
    origen = os.path.join(GRABACIONES_DIR, actual)
    destino = os.path.join(GRABACIONES_DIR, nuevo)
    if not os.path.exists(origen):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    if os.path.exists(destino):
        raise HTTPException(status_code=409, detail="Ya existe un archivo con ese nombre")
    os.rename(origen, destino)
    return True

def reproducir_grabacion(nombre: str, velocidad: float = 1.0, amplitud: float = 1.0):
    ruta = os.path.join(GRABACIONES_DIR, nombre)
    if not os.path.exists(ruta):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    y, sr = librosa.load(ruta, sr=SAMPLE_RATE)
    y_stretched = librosa.effects.time_stretch(y, rate=velocidad)
    y_amplificado = y_stretched * amplitud
    if np.max(np.abs(y_amplificado)) > 1.0:
        y_amplificado = y_amplificado / np.max(np.abs(y_amplificado)) * 0.95
    sd.play(y_amplificado, sr)
    sd.wait()
