from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from pathlib import Path
from app.rag import RAG

# load env variable
dotenv_path = Path('system.env')
load_dotenv(dotenv_path=dotenv_path)

# Initialize FastAPI app
app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the RAG system
data_directory = "data"
openai_api_key = os.getenv("OPENAI_API_KEY")
rag_system = RAG(data_directory=data_directory, openai_api_key=openai_api_key)

# Start the database listener
rag_system.start_listener()

@app.get("/", response_class=HTMLResponse)
async def read_auth():
    with open("static/login.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

class Question(BaseModel):
    question: str

class Answer(BaseModel):
    answer: str

@app.post("/ask", response_model=Answer)
def ask_question(question: Question):
    try:
        answer = rag_system.qa_system.run(question.question)
        return Answer(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")