from pydantic import BaseModel
from typing import List

class Answer(BaseModel):
    id: str = ""
    name: str = ""
    correct_answer: bool = False
    question_id: str = ""

class Question(BaseModel):
    id: str = ""
    name: str = ""
    answers: List[Answer] = []
    quiz_id: str = ""

class Quiz(BaseModel):
    id: str = ""
    name: str = ""
    questions : List[Question] = []

