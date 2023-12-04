from fastapi import APIRouter
from models.note import Note
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from config.db import conn
from fastapi.templating import Jinja2Templates
from schema.note import noteEntity, notesEntity

note = APIRouter()
templates = Jinja2Templates(directory="templates")


@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    doc = conn.notes.notes.find({})
    newdocs = []
    for docs in doc:
        newdocs.append({
            "id": docs["_id"],
            "title": docs["title"],
            "desc": docs["desc"],
            "important": docs["important"]
        })
    return templates.TemplateResponse("index.html", {"request": request, "newdocs": newdocs})


@note.post("/")
async def create_item(request: Request):
    form = await request.form()
    formDict = dict(form)
    formDict["important"] = True if formDict.get("important") == "on" else False
    note = conn.notes.notes.insert_one(formDict)
    return {"success": True}



