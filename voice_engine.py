from faster_whisper import WhisperModel
import tempfile


model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


def transcribe_audio(audio_file):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as temp:

        temp.write(audio_file.getvalue())
        audio_path = temp.name

    segments, info = model.transcribe(audio_path)

    text = ""

    for segment in segments:
        text += segment.text

    return text.strip()