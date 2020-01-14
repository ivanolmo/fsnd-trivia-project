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
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

# Trivia API

## Getting Started
The Trivia API is based on REST principles. Each endpoint returns JSON formatted data, and 
currently requires no authentication.

The API is hosted locally, and its base address is http://localhost:3000.

## Error handling
Errors are returned as a JSON object, and are formatted as follows:

```
{
    "success": False,
    "error": 405,
    "message": "The method is not allowed for the requested URL."
}
```

The API will return one of the following errors when a request fails:
```
- 400 -- Bad Request - The request could not be understood by the server
- 404 -- Not Found - The requested resource could not be found
- 405 -- Method Not Allowed - The specified method is not allowed for the endpoint
- 422 -- Unprocessable - The request could not be processed
- 500 -- Internal Server Error - The server encountered an unexpected condition
```


## Requests

The Trivia API endpoints are accessed using HTTP requests. Each endpoint uses the appropriate HTTP verbs for the action 
it performs. This API uses the GET, POST, and DELETE methods.

##### Method/Action
- GET -- retrieves questions and/or categories
- POST -- creates new questions or searches for existing questions
- DELETE -- deletes questions

##### Responses
The API will return one of the following status codes when a request succeeds:
```
- 200 -- OK - request successful
- 201 -- Created - new question created successfully
```
## Endpoints

### GET /questions
- This endpoint returns a list of all questions and categories contained in the database. The results are paginated in 
groups of 10.
- Sample usage:
`curl http://localhost:3000/questions`
- The possible response codes for this endpoint are 200 if successful, or 404 if no questions are found.
- The results are formatted as follows (note: only one question and category are included in sample result to show the 
formatting, all categories and 10 paginated questions will be returned in actual usage):
```
{
    "categories": [
        {
            "id": 1,
            "type": "Science"
        },
        {
            ... remaining categories in the list ...
        }
    ],
    "current_category": null,
    "questions": [
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "questions": "What boxer's original name is Cassius Clay?"
        },
        {
        ... remaining questions in the list ...
        }
    ],
    "success": True,
    "total_questions": 29
}
```

### GET /questions/<int:question_id>
- Using the given question_id, this endpoint returns a single question with that id.
- Sample usage:
`curl http://localhost:3000/questions/5`
- The possible response codes for this endpoint are 200 if successful, or 404 if that question doesn't exist.
- The result is formatted as follows:

```
{
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
    "question_id": 5,
    "success": true
}
```

### GET /categories
- This endpoint returns a list of all categories contained in the database.
- Sample usage:
`curl http://localhost:3000/categories`
- The possible response codes for this endpoint are 200 if successful, or 404 if no categories are found.
- The results are formatted as follows:
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
    "total_categories": 6
}
```

### GET /categories/<int:category_id>/questions
- Using the given category_id, this endpoint returns a list of all questions in that specific category, the number of
questions in that category, and the current category.
- Sample usage:
`curl http://localhost:3000/categories/6/questions`
- The possible response codes for this endpoint are 200 if successful, or 404 if there are no questions in the category.
- The results are formatted as follows:
```
{
    "current_category": {
        "id": 6,
        "type": "Sports"
    },
    "questions": [
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        }
    ],
    "success": true,
    "total_in_category": 2,
    "total_questions": 29
}
```
### DELETE /questions/<int:question_id>
- Using the given question_id, this endpoint will delete that specific question from the database.
- Sample usage:
`curl -X DELETE http://localhost:3000/questions/5`
- The possible response codes for this endpoint are 200 if successful, or 422 if the question doesn't exist.
- The results are formatted as follows:
```
{
    "deleted_id": 5,
    "success": true,
    "total_questions": 29
}
```

### POST /questions
- This endpoint serves two purposes. The first is to add a new question to the database. The second is to search for a
question using a valid search term.

##### Adding a new question
- Send a JSON formatted request body to the endpoint, containing a question, answer, difficulty, and category. All 
fields are required.
- The possible response codes for this endpoint are 201 if successful, or 400 if the request body is missing a field or 
is not formatted properly.
- Sample request body when adding a new question:
```
{
    "question": "What is the question?",
    "answer": "This is the answer.",
    "category": 1,
    "difficulty": 5
}
```
- Sample usage:
`curl -X POST http://localhost:3000/questions -d '{"question": "What is the question?", "answer": "This is the answer.",
 "category": 6, "difficulty": 1}' -H "Content-Type: application/json"`
- The results are formatted as follows (note: only one question is included in sample result to show the formatting, 
10 paginated questions will be returned in actual usage):
```
{
    "created_id": 29,
    "new_question": {
        "answer": "This is the answer.",
        "category": 6,
        "difficulty": 5,
        "id": 29,
        "question": "What is the question?"
    },
    "questions": [
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, and then praise in the role of her beloved Lestat?"
        },
        {
            ... the next 10 paginated questions ...
        }
    ],
    "success": True,
    "total_questions": 29
}
```

##### Searching for a question
- Send a JSON formatted request body to the endpoint, containing a valid search term (any non-empty search term is 
valid). The search is case insensitive. This field is required.
- The possible response codes for this endpoint are 200 if successful, or 400 if the request body is missing a search 
term.
- Sample request body when searching for a question (note: alternating case used to show case insensitivity):
```
{
    "searchTerm": "tItLe"
}
```
- Sample usage:
`curl -X POST http://localhost:3000/questions -d '{"searchTerm": "tItLe"}' -H "Content-Type: application/json"`
- The search will return any result containing the search term in the question. The results are formatted as follows:
```
{
    "questions": [
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "questions": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with 
                            multi-bladed appendages?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why The Caged Bird Sings'?"
        }
    ],
    "search_term": "tItLe",
    "success": True,
    "total_matching_questions": 2,
    "total_questions": 29
}
```
#### POST /quizzes
- This endpoint handles the questions in the Trivia game. Sending a request will return a single question, either in a
specific category, or from a randomly chosen category.
- The JSON formatted request body should include a category ID, as well as a list of IDs of any previous questions
asked. It will only return questions whose IDs are not in the previous_questions list.
- The possible response codes for this endpoint are 200 if successful, 400 if the request body isn't formatted properly,
or 404 if there are no questions in the chosen category.
- Sample request body using category 3-Geography and the IDs of three previously asked questions:
```
{
    "quiz_category": {"id": 3},
    "previous_questions": [13, 14, 15]
}
```
- Sample usage:
```
curl -X POST http://localhost:3000/quizzes -d '{"quiz_category": {"id": 3}, "previous_questions": [13, 14, 15]}' -H
"Content-Type: application/json"
```



















































