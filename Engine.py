from openai import OpenAI
from ignore.apikey import key, model, base_url



def load_text(file_path):
    with open(file_path, "r") as f:
        return f.read()

def break_into_chunks(text, chunk_size=1000):
    """Split text into chunks of roughly chunk_size characters."""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]



def ScanText(text, api_key, model_name, base_url, questions):
    client = OpenAI(
        base_url=base_url,
        api_key=api_key
    )

    # chunks = break_into_chunks(text)

    messages = [
        {
            "role": "user",
            "content": (
                "You are a document analysis assistant. Analyze the following text "
                "and answer these questions: " + " ".join(questions) + ". "
                "Text will come in chunks labeled 'chunk 1', 'chunk 2', etc. "
                "When you see 'THE END OF INPUT STREAM', give your final answer with reasoning."
            )
        }
    ]
    text = break_into_chunks(text)
    # Send chunks one by one
    for idx, chunk in enumerate(text):
        print(f"Sending chunk {idx + 1}...")

        messages.append({
            "role": "user",
            "content": f"chunk {idx + 1}: {chunk}"
        })

        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=8192,
        )

        assistant_msg = response.choices[0].message

        messages.append({
            "role": "assistant",
            "content": assistant_msg.content
        })

    # Signal end of input
    messages.append({
        "role": "user",
        "content": "THE END OF INPUT STREAM"
    })

    final_response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=1000
    )

    final_answer = final_response.choices[0].message.content

    return final_answer


if __name__ == "__main__":
    answer = ScanText("Yo! my pal's jacket is neither red nor blue, the place from where we purchased has 4 colors with one quantity for each color. blue, green, yellow, and red. I purchased red.", key, model, base_url,  ["What is the color of my pal's jacket?"])
    print(answer)