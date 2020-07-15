# Full Stack Trivia API Project
this project consists in proposing several trivial questions intended for the users in order to test their knowledge.
the goal is to create an API and a set of tests to implement the following tasks:


* display questions with a limited number per page and per category, a question has its level of difficulty, its category and the answer (which can be displayed or hidden)
* delete question
* add questions
* search questions by keywords
* Play the quiz

# Getting Started
### Installing Dependencies
#### Frontend Dependencies
##### Installing Node and NPM

download and install Node from https://nodejs.com/en/download.

##### installing project dependencies

after cloning the project cd to frontend directory and run this command

```
    npm install
		
```

#### Backend Dependencies
install dependencies by naviging to the /backend directory and run this command:

```
    pip install -r requirements.txt
```

#### Database Setup 
Install and setup "PostgreSQL" on the system and create a database named trivia in the Postgres server.

```
	createdb trivia
	With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
	cd database
	psql trivia < database/trivia.psql
```

### Running the Frontend in Dev Mode


The frontend app was built using create-react-app. to run the app use the command 

```
    npm start
```

### Running the Server
From the backend directory run the server, execute:

```
	export FLASK_APP=flaskr
	export FLASK_ENV=development
	flask run
```
	
# API Reference
### Getting Started

	* Backend Base URL: http://127.0.0.1:5000/
	* Frontend Base URL: http://127.0.0.1:3000/
	* Authentication: This version does not require authentication or API keys.

### Error Handling
Errors are returned as JSON in the following format:

```
	{
		"success": False,
		"error": 404,
		"message": "resource not found"
	}
```

The API will return three types of errors:

* 400 – bad request
* 404 – resource not found
* 422 – unprocessable

### Endpoints/
##### GET /categories

Returns a list categories.

Sample: curl http://127.0.0.1:5000/categories


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
	  "success": true,
	  "total_categories": 6

  }
```		  

##### GET /questions
Fetches the questions to be displayed on the page using page number
Sample: curl http://127.0.0.1:5000/questions?page=2
	
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
  "questions": [
    {
      "answer": "Agra",
      "category": "3",
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": "2",
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": "2",
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": "2",
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": "2",
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": "1",
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": "1",
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "20",
      "category": "1",
      "difficulty": 1,
      "id": 25,
      "question": "How old are you ?"
    },
    {
      "answer": "Tunis",
      "category": "3",
      "difficulty": 3,
      "id": 26,
      "question": "Capital of Tunisia ?"
    },
    {
      "answer": "Paris",
      "category": "3",
      "difficulty": 1,
      "id": 63,
      "question": "Capital of France ?"
    }
  ],
  "success": true,
  "total_questions": 10
}
```
##### DELETE /questions/<int:question_id>

	Deletes a question by id using url parameters.
	
	Sample: curl http://127.0.0.1:5000/questions/6 -X DELETE
	
```
	  {
		  "deleted": 6, 
	  }
```

##### POST /questions
create a new question or return the search results

###### 1. create a new question
Adds a questions to the database

Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "what is the capital of france?", "answer": "Paris", "difficulty": 2, "category": "3" }'

```	
{
  "created": 164,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": "5",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": "5",
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": "4",
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": "6",
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": "6",
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": "4",
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": "3",
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": "3",
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 69
}
```
###### 2.search term 
Fetches questions based on the search term
Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}'

```
{
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ],
  "success": true,
  "total_questions": 69
}
```
##### GET /categories/<int:category_id>/questions

Fetches questions for the requested category

Sample: curl http://127.0.0.1:5000/categories/2/questions

```
{
  "current_catogory": "Art",
  "questions": [
    {
      "answer": "Escher",
      "category": "2",
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": "2",
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": "2",
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": "2",
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "total_questions": 69
}
```

##### POST /quizzes

Fetches a unique question for the quiz on selected category
Sample: curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{'previous_questions': [11, 66],'quiz_category': {'type': 'Sports', 'id': '6'}}'

```
{
  "error": 400,
  "message": "bad request",
  "success": false
}
```

# Authors
Chokri Samaali worked on the API and test suite to integrate with the frontend

Udacity provided the starter files for the project including the frontend as a project template for the Full Stack Web Developer Nanodegree.
