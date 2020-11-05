from namespaceserver import NameSpaceServer
from fastapi import FastAPI
from fastapi import File, UploadFile

app = FastAPI()

server = NameSpaceServer()


@app.post("/savefile")
def savefile(file: UploadFile = File(...)):
    return server.save_file(file)
