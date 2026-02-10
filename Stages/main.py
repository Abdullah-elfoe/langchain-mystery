from .stage_1.audio import transcribe_audio
from .stage_2.document import convert_to_txt
from Engine import ScanText, getThinking
from ignore.apikey import key, model, base_url


audios_thinking = []
documents_thinking = []
contexts = {
    "audios": None,
    "documents": None,
    "final_reasoning": None
}

def audio_intelligence_pipeline(audio_file_paths, questions):
    """
    Complete pipeline to transcribe audio and convert documents to text
    """
    transcribed_audios = []
    answer = ""
    for path in audio_file_paths:
        transcribed_audio = transcribe_audio(path)
        transcribed_audios.append(f"Audio file {path} transcribed as: {transcribed_audio}\n---------------------------\n")
    # answer = ScanText(transcribed_audio, api_key=None)
    for audio in transcribed_audios:
        answer += ScanText(
            audio, 
            api_key=key,
            model_name=model,
            base_url=base_url,
            questions=questions
            )
    audios_thinking.append(questions)
    audios_thinking.append(answer)
    
    return answer


def document_forensics_pipeline(document_file_paths, questions):
    """
    Complete pipeline to convert documents to text and analyze them
    """
    converted_documents = []
    answer = ""
    for path in document_file_paths:
        converted_document = convert_to_txt(path)
        converted_documents.append(f"Document file {path} converted to text as: {converted_document}\n---------------------------\n")

    for document in converted_documents:
        answer += ScanText(
            document, 
            api_key=key,
            model_name=model,
            base_url=base_url,
            questions=questions
            )
    documents_thinking.append(questions)
    documents_thinking.append(answer)
        
    # answer = ScanText(converted_document, api_key=None)
    return answer

def reasoning_pipeline(questions, document_file_paths=[]):
    """
    Pipeline to answer reasoning questions without any input documents or audio

    """
    contexts["audios"] = getThinking(api_key=key, model_name=model, base_url=base_url, content=audios_thinking) if audios_thinking else None
    contexts["documents"] = getThinking(api_key=key, model_name=model, base_url=base_url, content=documents_thinking)  if documents_thinking else None
        
    answer = document_forensics_pipeline(document_file_paths, questions)
    contexts["final_reasoning"] = getThinking(api_key=key, model_name=model, base_url=base_url, content=[questions, answer]) if audios_thinking else None

    print(contexts)

    return answer

    # answer = ScanText(
    #     "", 
    #     api_key=key,
    #     model_name=model,
    #     base_url=base_url,
    #     questions=questions
    #     )
    # return answer


def main():
    answer = audio_intelligence_pipeline(["Resources/audio.wav"], ["What is being discussed in these audios?"])
    print("Audio Intelligence Pipeline Answer:")
    print(answer)
    print(audios_thinking, documents_thinking)
    print(contexts)
    reasoning_pipeline(None, None)
    print("Reasoning Pipeline Answer:")
    print(contexts)


# main()