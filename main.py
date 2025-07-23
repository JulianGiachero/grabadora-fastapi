
from fastapi import FastAPI, Query
from pydantic import BaseModel
from utils import grabar_audio, listar_grabaciones, eliminar_grabacion, renombrar_grabacion, reproducir_grabacion

app = FastAPI()

class RenombrarRequest(BaseModel):
    actual: str
    nuevo: str

class ReproducirRequest(BaseModel):
    nombre: str
    velocidad: float = 1.0
    amplitud: float = 1.0

@app.get("/")
def root():
    return {"mensaje": "API de grabadora en FastAPI funcionando 🎙️"}

@app.get("/grabaciones")
def get_grabaciones():
    return listar_grabaciones()

@app.post("/grabar")
def post_grabar(segundos: int = Query(..., gt=0, lt=120)):
    archivo = grabar_audio(segundos)
    return {"grabacion_guardada": archivo}

@app.delete("/eliminar")
def delete_grabacion(nombre: str):
    eliminar_grabacion(nombre)
    return {"estado": "eliminado", "archivo": nombre}

@app.post("/renombrar")
def post_renombrar(data: RenombrarRequest):
    renombrar_grabacion(data.actual, data.nuevo)
    return {"estado": "renombrado", "de": data.actual, "a": data.nuevo}

@app.post("/reproducir")
def post_reproducir(data: ReproducirRequest):
    reproducir_grabacion(data.nombre, data.velocidad, data.amplitud)
    return {"estado": "reproduciendo", "archivo": data.nombre}
