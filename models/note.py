from pydantic import BaseModel
from pymongo import MongoClient

class Note(BaseModel):
    id: str
    title: str
    desc: str
    #important: bool = None


MONGO_URI = "mongodb+srv://nonameh454:Mera111@inotesproject.mgxfeve.mongodb.net/notes"
conn = MongoClient(MONGO_URI)
