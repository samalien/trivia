import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs--
  '''
  CORS(app)
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow--
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,PUT,PATCH,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.--
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories=Category.query.all()

    # put all categories in a dict
    all_categories={}
    for category in categories:
      all_categories[category.id]=category.type

    # if there are no categories abort 404
    if len(all_categories)==0:
      abort(404)

    # return data to view
    return jsonify({
      'success':True,
      'categories':all_categories,
      'total_categories':len(categories)
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  def paginate_questions ( request, selection) :
    page=request.args.get('page',1,type=int)

    # determine the questions for each page
    start=(page - 1)* QUESTIONS_PER_PAGE
    end=start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in selection]
    current_questions=formatted_questions[start:end]
    return current_questions

  @app.route('/questions',methods=['GET'])
  def get_questions():
    # get all questions and then paginate
    selection=Question.query.order_by(Question.id).all()
    current_questions=paginate_questions(request, selection)
    categories=Category.query.all()

    # put all categories in a dict
    all_categories={}
    for category in categories:
      all_categories[category.id]=category.type

    # if no questions
    if len(current_questions) ==0:
      abort(404)

    # return data to view
    return jsonify({
      'success':True,
      'questions':current_questions,
      'total_questions':len(current_questions),
      'categories':all_categories
    })
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>',methods=['DELETE'])
  def delete_question(question_id):
    try:
      # get the question
      question=Question.query.filter(Question.id==question_id).one_or_none()

      questions=Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, questions)

      # if no question found abort 404
      if question is None:
        abort(404)

      # delete the question
      question.delete()

      # return success response
      return jsonify({
        'success':True,
        'deleted':question_id,
        'questions':current_questions,
        'total_questions':len(questions)
      })
    except:
      # if problem deleting
      abort(422)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions' , methods=['POST'])
  def create_search_question():
    # load the request body
    body=request.get_json()

    # load data from body
    new_question = body.get('question',None)
    new_answer = body.get('answer',None)
    new_category = body.get('category',None)
    new_difficulty = body.get('difficulty',None)
    search=body.get('searchTerm',None)

    try:
      if search:
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
        current_questions = paginate_questions(request, selection)

        # return data to view
        return jsonify({
          'success':True,
          'questions':current_questions,
          'total_questions':len(Question.query.all())
        })
      else:
          # ensure all fields have data
          if new_category is None or new_difficulty is None or new_answer is None or new_question is None:
            abort(422)

          # create and insert new question
          question=Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
          question.insert()

          selection = Question.query.order_by(Question.id).all()
          current_questions = paginate_questions(request, selection)

          # return data to view
          return jsonify({
            'success':True,
            'created':question.id,
            'questions':current_questions,
            'total_questions':len(selection)
          })
    except:
      abort(422)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions' , methods=['GET'])
  def get_questions_by_category(category_id):
    # get the category by id
    category=Category.query.filter_by(id=category_id).one_or_none()

    # if category isn't found
    if category is None:
      abort(400)

    # get the matching questions
    questions=Question.query.filter(Question.category==str(category_id)).all()
    current_questions=paginate_questions(request, questions)

    # return data to view
    return jsonify({
      'success':True,
      'questions':current_questions,
      'total_questions':len(Question.query.all()),
      'current_catogory':category.type
    })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def get_questions_quiz():
    # load the request body
    body = request.get_json()

    # abort 400 if category or previous questions or body isn't found
    if body is None or body['previous_questions'] is None or body['quiz_category'] is None:
      abort(400)

    previous_questions=body['previous_questions']
    category=body['quiz_category']

    # if ALL is selected load all questions
    if category['id'] == 0:
      questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
    else:
      # load questions for given category
      questions =Question.query.filter(Question.id.notin_(previous_questions), Question.category == category['id']).all()


    if len(questions)==0 or questions is None:
      question=None
    else:
      #  get random question
      choice=random.randint(0, len(questions)-1)
      question=questions[choice]

    # return data to view
    return jsonify({
      'success':True,
      'question':question.format() if question != None else None
    })




  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success':False,
      'error':404,
      'message':'Resource not found'
    }),404
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success':False,
      'error':422,
      'message':' unprocessible '
    }),422

  @app.errorhandler(400)
  def bad_request (error):
    return jsonify({
      'success':False,
      'error':400,
      'message': 'bad request'
    }),400
  return app
