# QuizApp
## How to run?
1. Clone the repo.
2. Run `main.py`.
3. Run the server `uvicorn main:app --reload`.
4. Check FastApi docs `http://127.0.0.1:8000/docs`.

## Sample of add quiz request body:
```
{
    "name": "Quiz 1",
    "questions": [
      {
        "name": "question 1",
        "answers": [
          {
            "name": "answer 1",
            "correct_answer": 0
          },
          {
            "name": "answer 2",
            "correct_answer": 1
          },
          {
            "name": "answer 3",
            "correct_answer": 0
          }
        ]
      },
      {
        "name": "question 2",
        "answers": [
          {
            "name": "answer 1",
            "correct_answer": 0
          },
          {
            "name": "answer 2",
            "correct_answer": 1
          },
          {
            "name": "answer 3",
            "correct_answer": 0
          }
        ]
      }
    ]
  }
  ```

  ## Sample of solve quiz request body:
  ```
{
    "quiz_id": 1,
    "questions": [
      {
        "question_id": 1,
         "answer_id": 1
      },
      {
        "question_id": 4,
        "answer_id": 2
      }
    ]
  }
  ```