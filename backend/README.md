# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Get a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
the following example record is based on trivia.psql data
{
  "categories": {
    {
       "id": 1,
        "type": "Science"
    },
    {
        "id": 2,
        "type": "Art"
    },
    {
        "id": 3,
        "type": "Geography"
    },
    {
        "id": 4,
        "type": "History"
    },
    {
        "id": 5,
        "type": "Entertainment"
    },
    {
        "id": 6,
        "type": "Sports"
    }
    },
    "total_categories": 6,
    "success": true
}


POST '/categories'
- Create a Category into our database
- Request Arguments: an object with key, catname that will be used to be inserted into the db
- Returns: Created catname with state of success as Boolean
{
  "categories": [
  {
    "catname": "Science",
  }
  ],
  "Created": Science,
  "success": true
}


GET '/questions'
- Get a dictionary of questions in which the keys are the ids and the values is the corresponding string of the question, string of the answer,
integer of category and integer of difficulty
- Request Arguments: None
- Returns: An object with questions, that each contains an object array of question id, question category id, question difficulty, question answer, and question, text.
an object array of categories, total questions integer, success as Boolean.
the following example record is based on trivia.psql data
{
  "questions": [
      {
        "answer": "Apollo 13",
        "category": 5,
        "difficulty": 4,
        "id": 2,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
      },
      {
        "answer": "Muhammad Ali",
        "category": 4,
        "difficulty": 1,
        "id": 9,
        "question": "What boxer's original name is Cassius Clay?"
      },
      {
        "answer": "Lake Victoria",
        "category": 3,
        "difficulty": 5,
        "id": 13,
        "question": "What is the largest lake in Africa?"
      }
      {
        "answer": "Mona Lisa",
        "category": 2,
        "difficulty": 3,
        "id": 17,
        "question": "La Giaconda is better known as what?"
      }
      ],
      "total_questions": 4,
      "categories": [
      {
        "id": 1,
        "type": "Science"
      }
      {
        "id": 2,
        "type": "Art"
      }
      {
        "id": 3,
        "type": "Geography"
      }
      {
        "id": 4,
        "type": "History"
      }
      ],
      "success": true
}

DELETE '/questions/<int:questionid>'
- Delete a question based on questionid which is the id of the question .
that we want to delete
- Request Arguments: int:question_id
- Returns: the deleted question id , success as Boolean
{
  "deleted": 1,    
  "success": true
}

POST '/questions'
- Create a New Question into our database
- Request Arguments: an object with key, question, answer, category, difficulty,
that will be used to be inserted into the db
- Returns: Created question with state of success as Boolean
{
  "questions": [
  {
   "answer": "Maybe",
    "category": 5,
    "difficulty": 4,
    "question": "are we going to mars in 2050 ?"
  }
  ],
  "Created": are we going to mars in 2050 ?,
  "success": true
}


POST '/questions/search'
- Get a dictionary of questions based on the searchTerm
- Request Arguments: An object with a key searchTerm
- Returns: all questions that are matched with the searchterm keyword
the following example record is based on trivia.psql data
{
  "questions": [
      {
        "answer": "Apollo 13",
        "category": 5,
        "difficulty": 4,
        "id": 2,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
      },
      {
        "answer": "Muhammad Ali",
        "category": 4,
        "difficulty": 1,
        "id": 9,
        "question": "What boxer's original name is Cassius Clay?"
      },
      {
        "answer": "Lake Victoria",
        "category": 3,
        "difficulty": 5,
        "id": 13,
        "question": "What is the largest lake in Africa?"
      }
      {
        "answer": "Mona Lisa",
        "category": 2,
        "difficulty": 3,
        "id": 17,
        "question": "La Giaconda is better known as what?"
      }
      ],
      "total_questions": 4,
      "success": true
}

GET '/categories/<int:catid>/questions'
- Get a dictionary of questions based on the given catid
- Request Arguments: An object with a key, category that contains id of the category of the questions to list: category_id key:value pairs.
- Returns: current_category that is included in the parameter value[catid]
an object array that holds questions found, total questions number, categories that based on the given id
{
  "current_category": "3",
  "questions": [
    {
      "answer": "an answer of the question",
      "category": 3,
      "difficulty": <difficulty of the question >,
      "id": <id of the question>,
      "question": "the question from that category"
    }
    ],
  "success": true,
  "total_questions": 2
}

POST '/quizzes'
- Get a dictionary of questions based on given category and previous question parameters and return a random questions within the given category,
and that is not one of the previous questions.
- Request Arguments: An object with a Valid key, category that contains id of the category of the questions,
- Returns: previousQuestions, question, question difficulty, question answer, and question text.
{
  "previousQuestions": [1, 2],
  "question": {
      "answer": "an answer of the question",
      "category": <category of the question>,
      "difficulty": <difficulty of the question >,
      "id": <id of the question>,
      "question": "the question from that category"
      },
  "success": true
}

```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
