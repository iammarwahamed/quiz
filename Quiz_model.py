import sqlite3
from fastapi import  Request
from Quiz_classes import Answer, Question, Quiz

class Quiz_model:

    def __init__(self):
        self.conn = sqlite3.connect("database/Quiz.db")
        self.conn.row_factory = sqlite3.Row
        self.cur =  self.conn.cursor()

    def get_quizzes(self):
        quizList = []
        self.cur.execute('SELECT * FROM QUIZZES;')
        quizzes = self.cur.fetchall()
        for quiz in quizzes:
             quizObj = {
                'id': quiz['id'],
                'name': quiz['name'],
                'questions': self.get_quiz_question(quiz['id'])
             }
             quizList.append(quizObj)
        return quizList 

    def get_quiz(self, id):
        quiz = []
        query = f'SELECT * FROM QUIZZES WHERE id = "{id}" ;'
        self.cur.execute(query)
        quizObj = self.cur.fetchone()
        
        if quizObj is None:
            return quiz
        else:
            quiz = {
                'id': quizObj['id'],
                'name': quizObj['name'],
                'questions': self.get_quiz_question(quizObj['id'])
            }    

        return quiz
    def get_quiz_question(self, quiz_id):
        questionList = []
        query = f'SELECT * FROM QUESTIONS WHERE Quiz_id="{quiz_id}" ;'
        self.cur.execute(query)
        questions = self.cur.fetchall()

        for question in questions:
            questionObj = {
                'id': question['id'],
                'name': question['name'],
                'correct_answer_id' : question['correct_answer_id'],
                'answers': self.get_question_answers(question['id'])
            }
            questionList.append(questionObj)

        return questionList;

    def get_question_answers(self, question_id):
        answersList = []
        query = f'SELECT * FROM  ANSWERS WHERE Question_id = "{question_id}";'
        self.cur.execute(query)
        answers = self.cur.fetchall()

        for answer in answers:
            answerObj = {
                'id': answer['id'],
                'name': answer['name'],
            }
            answersList.append(answerObj)

        return answersList;

    def add_quiz(self, quiz: Quiz):
        self.cur.execute(f'INSERT INTO QUIZZES ("name") VALUES ("{quiz["name"]}");')
        quiz_id = self.cur.lastrowid

        for question in quiz['questions']:
            self.add_question(question, quiz_id)

        return quiz_id

    def add_question(self, question: Question, quiz_id: int):
        self.cur.execute(f'INSERT INTO Questions ("name", "quiz_id") VALUES ("{question["name"]}", "{quiz_id}");')
        question_id = self.cur.lastrowid

        for answer in question['answers']:
            answer_id = self.add_answer(answer, question_id)
            if(answer["correct_answer"]): 
                    self.cur.execute(f'UPDATE Questions SET correct_answer_id = "{answer_id}" WHERE id = "{question_id}"');

        return question_id

    def add_answer(self, answer: Answer, question_id: int):
        self.cur.execute(f'INSERT INTO ANSWERS ("name", "question_id") VALUES ("{answer["name"]}", "{question_id}");')
        answer_id = self.cur.lastrowid

        return answer_id;

    def delete_quiz(self, id: int):
        self.cur.execute(f'DELETE FROM ANSWERS WHERE Question_id in (select id from QUESTIONS WHERE Quiz_id="{id}");')
        self.cur.execute(f'DELETE FROM QUESTIONS WHERE Quiz_id="{id}" ;')
        self.cur.execute(f'DELETE FROM QUIZZES WHERE id = "{id}" ;')
        self.close_conn()

    def view_quiz(self, id):
        quiz = self.get_quiz(id)
        #delete ids
        del quiz["id"]
        for question in quiz['questions']:
              del question["id"]
              del question["correct_answer_id"]
              for answer in question['answers']:
                  del answer["id"]
        return quiz

    def solve_quiz(self, questions_solved: dict ):
        count = 0
        for question_solved in questions_solved['questions']:
            query = f'SELECT correct_answer_id FROM  QUESTIONS WHERE id = "{question_solved["question_id"]}";'
            self.cur.execute(query)
            correct_answer_id = self.cur.fetchone()
            if(correct_answer_id["correct_answer_id"] == question_solved["answer_id"]):
                count = count+1

        return count  
    def create_demo(self):
        #self.cur.execute('DROP TABLE IF EXISTS ANSWERS')
        #self.cur.execute('DROP TABLE IF EXISTS QUESTIONS')
        #self.cur.execute('DROP TABLE IF EXISTS QUIZZES')
        self.cur.execute('CREATE TABLE QUIZZES (id INTEGER PRIMARY KEY,  NAME TEXT(40));')
        self.cur.execute('INSERT INTO QUIZZES VALUES (1,"Quiz 1");')
        self.cur.execute('INSERT INTO QUIZZES VALUES (2,"Quiz 2");')
        self.cur.execute('CREATE TABLE QUESTIONS (id INTEGER PRIMARY KEY, NAME TEXT(40), Quiz_id INTEGER, CORRECT_ANSWER_ID INTEGER);')
        self.cur.execute('INSERT INTO QUESTIONS VALUES (1,"question 1",1,1);')
        self.cur.execute('INSERT INTO QUESTIONS VALUES (2,"question 2",1,4);')
        self.cur.execute('INSERT INTO QUESTIONS VALUES (3,"question 1",2,7);')
        self.cur.execute('INSERT INTO QUESTIONS VALUES (4,"question 2",2,11);')
        self.cur.execute('CREATE TABLE ANSWERS (id INTEGER PRIMARY KEY, NAME TEXT(10), Question_id INTEGER);')
        self.cur.execute('INSERT INTO ANSWERS VALUES (1,"answer 1",1);')
        self.cur.execute('INSERT INTO ANSWERS VALUES (2,"answer 2",1);')
        self.cur.execute('INSERT INTO ANSWERS VALUES (3,"answer 3",1);')
        self.cur.execute('INSERT INTO ANSWERS VALUES (4,"answer 1",2);')
        self.cur.execute('INSERT INTO ANSWERS VALUES (5,"answer 2",2);')
        self.cur.execute('INSERT INTO ANSWERS VALUES (6,"answer 3",2);')
        self.cur.execute('INSERT INTO ANSWERS VALUES (7,"answer 1",3);')
        self.cur.execute('INSERT INTO ANSWERS VALUES (8,"answer 2",3);')
        self.cur.execute('INSERT INTO ANSWERS VALUES (9,"answer 3",3);')
        self.cur.execute('INSERT INTO ANSWERS VALUES (10,"answer 1",4);')
        self.cur.execute('INSERT INTO ANSWERS VALUES (11,"answer 2",4);')
        self.cur.execute('INSERT INTO ANSWERS VALUES (12,"answer 3",4);')
        self.close_conn() 


    def close_conn(self):
        self.conn.commit()
        #self.cur.close()
        #self.conn.close()          
