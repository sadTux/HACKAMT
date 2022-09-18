from importlib import import_module
from urllib import response
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import uuid
import base64
import cv2



app = FastAPI()


async def save_image(file:str):
    name = str(uuid.uuid4())
    file_data = file.split(",")[-1]
    with open(name, "wb") as f:
        f.write(base64.b64encode(file_data))
    return name

class FileData(BaseModel):
    file: str

class Analyzer(BaseModel):
    quantidade_aluno: int
    



@app.post("/base", response_model=Analyzer)
async def analyze_route(data: FileData):
    name = str(uuid.uuid4())
    file_data = data.file.split(",")[-1]
    with open(name, "wb") as f:
        f.write(base64.b64decode(file_data))

    face_cascade = cv2.CascadeClassifier('/home/mateus/Documentos/teste/haarcascade_frontalface_alt.xml')
    img = cv2.imread(name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    print (len(faces))

    response = Analyzer(quantidade_aluno=len(faces))
    return response

@app.post("/mimi", response_model=Analyzer)
async def analyze_route(file: UploadFile = File(...)):
    name = str(uuid.uuid4())
    with open(name, "wb") as f:
        f.write(await file.read())

    face_cascade = cv2.CascadeClassifier('/home/mateus/Documentos/teste/haarcascade_frontalface_alt.xml')
    img = cv2.imread(name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) == 0:
        return ("No faces found")

    else:
        response = Analyzer(quantidade_aluno=len(faces))
  
        return response


