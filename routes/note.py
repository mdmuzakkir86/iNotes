from fastapi import APIRouter, Request, Form, Response
from models.note import conn
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId


note = APIRouter()
templates = Jinja2Templates(directory="templates")

@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@note.post("/", response_class=HTMLResponse)
async def add_notes(request: Request):
    form = await request.form()
    print(form)
    formDict = dict(form)
    formDict["important"] = True if formDict.get("important") == "on" else False
    note = conn.notes.notes.insert_one(dict(formDict))
    return templates.TemplateResponse("result.html", {"request": request, "message": "Added successfully!"})

@note.get("/getnotes", response_class=HTMLResponse)
async def get_notes(request: Request):
    docs = conn.notes.notes.find({})
    newDocs = []
    for doc in docs:
        #print("doc:",doc)
        newDocs.append({
            "_id": doc["_id"],
            "title": doc["title"],
            "desc": doc["desc"],
            "important": doc["important"]  
        })
    return templates.TemplateResponse("getnotes.html", {"request": request, "newDocs":newDocs})


@note.get("/edit/{id}",response_class=HTMLResponse)
def edit_note(id:str,response:Response,request:Request):
    print(" method called :"+str(id))
    docs = conn.notes.notes.find({})
    note = {}
    for doc in docs:
        if str(doc["_id"]) == id:
            # print(doc)
            note["_id"]= doc["_id"]
            note["title"]= doc["title"]
            note["desc"]= doc["desc"]
            note["important"]= doc["important"]
    #print(note)
    return templates.TemplateResponse("edit_notes.html", {"request": request, "note": note})


@note.post("/update", response_class=HTMLResponse)
async def update_note(request:Request, noteId: str = Form(...), noteTitle: str = Form(...), noteDesc: str = Form(...)):
    try:
        
        # Convert noteId to ObjectId
        note_id = ObjectId(noteId)

        # Update the note in MongoDB based on the converted noteId
        result = conn.notes.notes.update_one({"_id": note_id}, {"$set": {"title": noteTitle, "desc": noteDesc}})

        if result.matched_count > 0:
            message = "Note updated successfully."
        else:
            message = "Note update failed."
    except Exception as e:
        message = f"Error: {str(e)}"
    
    return templates.TemplateResponse("result.html", {"request":request,"message": message})


@note.get("/delete/{id}",response_class=HTMLResponse)
def delete_fish(id:str,request:Request):
    print(" delete fish method called :"+str(id))
    note_id = ObjectId(id)
    result = conn.notes.notes.delete_one({'_id':note_id})
    return templates.TemplateResponse("result.html", {"request": request, "message": "Deleted successfully!"})

    