import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader


INPUT_DIR = "/home/abdullah/Desktop/Playground/langchain/ap2/Resources"
OUTPUT_DIR = "txt_output"


def ensure_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def convert_pdf(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    text = "\n\n".join(doc.page_content for doc in docs)
    return text


def convert_docx(file_path):
    loader = Docx2txtLoader(file_path)
    docs = loader.load()

    text = "\n\n".join(doc.page_content for doc in docs)
    return text


def save_txt(filename, text):
    txt_path = os.path.join(OUTPUT_DIR, filename)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)


def convert_to_txt(file):
    ensure_dirs()

    # file_path = os.path.join(INPUT_DIR, file)
    file_path = file
    # print(file_path)

    if file_path.lower().endswith(".pdf"):
        # print(f"Processing PDF: {file}")
        text = convert_pdf(file_path)
        # save_txt(file.replace(".pdf", ".txt"), text)

    elif file_path.lower().endswith(".docx"):
        print(f"Processing DOCX: {file}")
        text = convert_docx(file_path)
        # save_txt(file.replace(".docx", ".txt"), text)

    else:
        # print(f"Skipping unsupported file: {file}")
        text = None
    return text


if __name__ == "__main__":
    # files = os.listdir(INPUT_DIR)
    print(INPUT_DIR, "f")
    # print(files)
    for file in os.listdir("Resources"):
        print(convert_to_txt(file))
