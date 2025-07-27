from pydub import AudioSegment

def procesar_audio(input_path: str, output_path: str, velocidad: float, volumen: float):
    audio = AudioSegment.from_file(input_path)

    # Cambiar velocidad
    audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * velocidad)
    }).set_frame_rate(audio.frame_rate)

    # Cambiar volumen
    audio = audio + (20 * (volumen - 1))  # Aproximado para dB

    audio.export(output_path, format="wav")