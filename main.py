from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import shutil
import os
from documentScanner import ScanText

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
questions_for_llm = ["No questions enjoy. Just tell me about my diaper"]

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze/")
async def analyze(request: Request, file: UploadFile = File(...), questions: str = ""):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    questions_list = [q.strip() for q in questions.split(",") if q.strip()]
    if len(questions_for_llm) > 0:
        questions_for_llm.clear()
        questions_for_llm.extend(questions_list)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)



    # 🔥 Here you call your AI pipeline
    result = f"File {file.filename} received."
    print(UPLOAD_DIR + "/" + file.filename)
    
    result = ScanText(UPLOAD_DIR + "/" + file.filename, "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", 
    questions_for_llm
)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": result}
    )
