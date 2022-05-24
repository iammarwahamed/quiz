from fastapi import FastAPI, status
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import Json
from starlette.responses import  RedirectResponse
from Quiz_classes import Quiz

from Quiz_model import Quiz_model


app = FastAPI()
templates = Jinja2Templates(directory="html")
quiz_model = Quiz_model()


#http://127.0.0.1:8000/createDemo
@app.get("/createDemo",status_code=status.HTTP_200_OK)
async def create_demo():
    quiz_model.create_demo()
    return quiz_model.get_quizzes()


#http://127.0.0.1:8000/list
@app.get("/quiz/list", status_code=status.HTTP_200_OK,tags=['quiz'])
async def get_list():
    return quiz_model.get_quizzes()

@app.post("/quiz/add", status_code=status.HTTP_201_CREATED, tags=['quiz'])
async def add_quiz(quiz: Quiz):
    return quiz_model.add_quiz(quiz.dict())

@app.get("/quiz/view/{id}", status_code=status.HTTP_200_OK, tags=['quiz'])
async def view_quiz(id: int):
    return quiz_model.view_quiz(id)

@app.put("/quiz/solve", status_code=status.HTTP_201_CREATED, tags=['quiz'])
async def solve_quiz(questions_solved: dict):
    return quiz_model.solve_quiz(questions_solved)

@app.delete("/quiz/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=['quiz'])
async def delete_quiz(id: int):
    quiz_model.delete_quiz(id)
   





# uvicorn main:app --reload