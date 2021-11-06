from fastapi import FastAPI,UploadFile,File,Request,Body
import shutil
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from starlette.responses import StreamingResponse
import io
import spacy
from summerizer import calculate_sentences_score,calculate_word_frequency,summerize,normalize


app = FastAPI()
nlp = spacy.load("en_core_web_sm")

templates=Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root(request:Request):
    return templates.TemplateResponse("home.html",{"request":request})

@app.post("/")
async def root(text):
    nlp=spacy.load("en_core_web_sm")
    docx=nlp(text)
    words_freaquency=calculate_word_frequency(docx)
    normalize(words_freaquency)
    sentences_score=calculate_sentences_score(docx,words_freaquency)
    return(summerize(sentences_score))
