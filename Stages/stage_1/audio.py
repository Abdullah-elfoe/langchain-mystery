import whisper
import os


def transcribe_audio(file_path):
    """
    Transcribe a single audio file using Whisper
    """

    print("Loading Whisper model...")

    # Load model (automatically downloads if first time)
    model = whisper.load_model("base")

    print(f"Transcribing: {file_path}")

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File not found: {file_path}")
        return None

    # Transcribe
    result = model.transcribe(file_path)

    # Print results
    # print("\n" + "=" * 60)
    # print("TRANSCRIPTION COMPLETE")
    # print("=" * 60)
    # print(f"Text: {result['text']}")
    # print(f"Language: {result.get('language', 'unknown')}")
    # print(f"Duration: {result.get('duration', 0):.2f} seconds")

    # Save to file
    # with open("transcription.txt", "w", encoding="utf-8") as f:
    #     f.write(result["text"])

    # print("\nSaved to: transcription.txt")
    return result["text"]


# Run it
if __name__ == "__main__":
    # CHANGE THIS TO YOUR ACTUAL FILE PATH
    audio_file = "../../Resources/audio.ogg"  # or "audio.mp3", "audio.wav", etc.

    # Transcribe
    transcript = transcribe_audio(audio_file)

