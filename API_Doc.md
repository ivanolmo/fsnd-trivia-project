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
### POST /quizzes
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
