import whisper
import os

WHISPER_MODEL=os.getenv("WHISPER_MODEL","small")

_model=None
def load_model():
    global _model

    if _model is None:
        print("loading model...")
        _model= whisper.load_model(WHISPER_MODEL)
        print("whisper model loaded successfully")

    return _model

def transcribe_chunk(chunk_path: str, translate: bool = False):

    model = load_model()

    task = "translate" if translate else "transcribe"

    try:

        result = model.transcribe(
            chunk_path,
            task=task
        )

        return result["text"]

    except Exception as e:

        print(f"Error transcribing {chunk_path}")

        print(e)

        return ""



def transcribe_all(chunks: list, translate: bool = False):

    full_transcript = ""

    for i, chunk in enumerate(chunks):

        print(f"Transcribing chunk {i+1}")

        # Check if file exists
        if not os.path.exists(chunk):
            print(f"Chunk does not exist: {chunk}")
            continue

        # Check for empty chunk
        if os.path.getsize(chunk) == 0:
            print(f"Skipping empty chunk: {chunk}")
            continue

        try:
            text = transcribe_chunk(chunk, translate=translate)

            full_transcript += text + " "

        except Exception as e:

            print(f"Error while transcribing {chunk}")

            print(e)

            continue

    print("Transcription Completed")

    return full_transcript