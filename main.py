from namespaceserver import NameSpaceServer
from fastapi import FastAPI
from fastapi import File, UploadFile, Response
from starlette.responses import FileResponse
from fastapi.responses import StreamingResponse
from tempfile import SpooledTemporaryFile
app = FastAPI()

server = NameSpaceServer()


@app.post("/savefile")
def savefile(file: UploadFile = File(...)):
    return server.save_file(file)


@app.get("/getfile")
def getfile(filename: str):
    return StreamingResponse(server.get_file(filename), media_type='multipart/mixed', headers={'Content-Disposition': f'inline; filename="{filename}"'})
