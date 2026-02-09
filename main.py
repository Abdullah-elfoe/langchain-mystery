from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from Stages.main import audio_intelligence_pipeline
from Stages.main import document_forensics_pipeline


app = FastAPI()

app.mount("/static", StaticFiles(directory="ui/static"), name="static")
templates = Jinja2Templates(directory="ui/templates")

# Get functions for each page

@app.get("/", response_class=HTMLResponse)
def read_root(request:Request):
    return templates.TemplateResponse(
        "home.html", {"request": request}
        )

@app.get("/audio-intelligence", response_class=HTMLResponse)
def audio_intelligence(request:Request):
    return templates.TemplateResponse(
        "audio-intelligence.html", {"request": request}
        )

@app.get("/document-forensics", response_class=HTMLResponse)
def document_forensics(request:Request):
    return templates.TemplateResponse(
        "document-forensics.html", {"request": request}
        )

@app.get("/reasoning", response_class=HTMLResponse)
def reasoning(request:Request):
    return templates.TemplateResponse(
        "reasoning.html", {"request": request}
        )


# post methods for each pipeline will go here

@app.post("/audio-intelligence", response_class=HTMLResponse)
async def audio_intelligence_post(request:Request):
    form_data = await request.form()
    audio_files = form_data.getlist('audio_files')
    if audio_files is not None:
        result = True
    else:

        result = False
    
    # Process the audio files using the audio intelligence pipeline
    result = audio_intelligence_pipeline([f"Resources/{file}" for file in audio_files])
    result = "".join(result)
    return templates.TemplateResponse(
        "audio-intelligence.html", {"request": request, "result": result}
        )


@app.post("/document-forensics", response_class=HTMLResponse)
async def document_forensics_post(request:Request):
    form_data = await request.form()
    document_files = form_data.getlist('document_files')
    # Process the document files using the document forensics pipeline
    result = document_forensics_pipeline([f"Resources/{file}" for file in document_files])
    result = "".join(result)
    return templates.TemplateResponse(
        "document-forensics.html", {"request": request, "result": result}
        )