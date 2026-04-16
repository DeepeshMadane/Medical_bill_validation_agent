from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import shutil

from rag.vector_db import create_vector_db, get_retriever
from agent.langgraph_agent import build_graph

app = FastAPI()

# -------------------------------
# LOAD AGENT
# -------------------------------
vector_db = create_vector_db("data/final_hospital_tariff_dataset.xlsx")
retriever = get_retriever(vector_db)
agent = build_graph(retriever)

# -------------------------------
# SERVE UI
# -------------------------------
app.mount("/ui", StaticFiles(directory="ui"), name="ui")

@app.get("/")
def home():
    return FileResponse("ui/index.html")


# -------------------------------
# API
# -------------------------------
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = agent({"image_path": file_path})

    return result["results"]