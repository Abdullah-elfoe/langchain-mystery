from openai import OpenAI



def load_text(file_path):
    with open(file_path, "r") as f:
        return f.read()

def break_into_chunks(text, chunk_size=1000):
    """Split text into chunks of roughly chunk_size characters."""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# def ScanText(text, api_key, questions):
#     client = OpenAI(
#         base_url="https://openrouter.ai/api/v1",
#         api_key=api_key,
#     )

#     data = text
#     chunks = break_into_chunks(data)

#     messages = [
#         {
#             "role": "user",
#             "content": (
#                 "You are a document analysis assistant. Analyze the following text "
#                 "and answer these questions: "+ " ".join(questions) + ". "
#                 "Text will come in chunks labeled 'chunk 1', 'chunk 2', etc. "
#                 "When you see 'THE END OF INPUT STREAM', give your final answer with reasoning."
#             )
#         }
#     ]

#     # Send each chunk sequentially
#     for idx, chunk in enumerate(chunks):
#         print(f"Sending chunk {idx+1}: {chunk[:50]}...")
#         messages.append({"role": "user", "content": f"chunk {idx+1}: {chunk}"})
#         response = client.chat.completions.create(
#             model="deepseek/deepseek-v3.2",
#             messages=messages,
#             max_tokens=1000,
#             extra_body={"reasoning": {"enabled": True}}
#         )
#         response_msg = response.choices[0].message
#         messages.append({
#             "role": "assistant",
#             "content": response_msg.content,
#             "reasoning_details": response_msg.reasoning_details
#         })

#     # End of input
#     messages.append({"role": "user", "content": "THE END OF INPUT STREAM"})
#     final_response = client.chat.completions.create(
#         model="deepseek/deepseek-v3.2",
#         messages=messages,
#         max_tokens=1000,
#         extra_body={"reasoning": {"enabled": True}}
#     )

#     final_msg = final_response.choices[0].message.content
#     with open("final.txt", "w") as f:
#         f.write(final_msg)

#     print("END OF INPUT STREAM SENT. FINAL RESPONSE:")
#     return final_msg



def ScanText(text, api_key, questions):
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
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
            model="deepseek-ai/deepseek-v3.2",
            messages=messages,
            max_tokens=8192,
            extra_body={"chat_template_kwargs": {"thinking": True}}
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
        model="deepseek-ai/deepseek-v3.2",
        messages=messages,
        max_tokens=1000,
        extra_body={"chat_template_kwargs": {"thinking": True}}
    )

    final_answer = final_response.choices[0].message.content

    return final_answer


if __name__ == "__main__":
    answer = ScanText("Yo! my pal's jacket is neither red nor blue, the place from where we purchased has 4 colors with one quantity for each color. blue, green, yellow, and red. I purchased red.", "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", ["What is the color of my pal's jacket?"])
    print(answer)