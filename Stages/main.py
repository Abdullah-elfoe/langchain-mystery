from .stage_1.audio import transcribe_audio
from .stage_2.document import convert_to_txt
from Engine import ScanText


def audio_intelligence_pipeline(audio_file_paths):
    """
    Complete pipeline to transcribe audio and convert documents to text
    """
    transcribed_audios = []
    for path in audio_file_paths:
        transcribed_audio = transcribe_audio(path)
        transcribed_audios.append(f"Audio file {path} transcribed as: {transcribed_audio}\n---------------------------\n")
    # answer = ScanText(transcribed_audio, api_key=None)
    return transcribed_audios


def document_forensics_pipeline(document_file_paths):
    """
    Complete pipeline to convert documents to text and analyze them
    """
    converted_documents = []
    for path in document_file_paths:
        converted_document = convert_to_txt(path)
        converted_documents.append(f"Document file {path} converted to text as: {converted_document}\n---------------------------\n")
    # answer = ScanText(converted_document, api_key=None)
    return converted_documents