from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from utils import procesar_audio
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODULATED_DIR = "modulated_audio"
os.makedirs(MODULATED_DIR, exist_ok=True)

@app.post("/modulate")
async def modulate_audio(
    file: UploadFile = File(...),
    velocidad: float = Form(...),
    volumen: float = Form(...)
):
    filename = file.filename
    output_path = os.path.join(MODULATED_DIR, f"mod_{filename}")

    try:
        contents = await file.read()
        with open(filename, "wb") as f:
            f.write(contents)

        procesar_audio(filename, output_path, velocidad, volumen)
        os.remove(filename)

        return FileResponse(output_path, media_type="audio/wav", filename=f"mod_{filename}")

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/list")
def listar_audios():
    files = os.listdir(MODULATED_DIR)
    return {"archivos": files}

@app.get("/download/{filename}")
def descargar(filename: str):
    path = os.path.join(MODULATED_DIR, filename)
    if os.path.exists(path):
        return FileResponse(path, media_type="audio/wav", filename=filename)
    return JSONResponse(content={"error": "Archivo no encontrado"}, status_code=404)