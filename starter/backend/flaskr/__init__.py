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

    CORS(app)
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,PUT,PATCH,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()

        # put all categories in a dict
        all_categories = {}
        for category in categories:
            all_categories[category.id] = category.type

        # if there are no categories abort 404
        if len(all_categories) == 0:
            abort(404)

        # return data to view
        return jsonify({
            'success': True,
            'categories': all_categories,
            'total_categories': len(categories)
        })

    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)

        # determine the questions for each page
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        formatted_questions = [question.format() for question in selection]
        current_questions = formatted_questions[start:end]
        return current_questions

    @app.route('/questions', methods=['GET'])
    def get_questions():
        # get all questions and then paginate
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories = Category.query.all()

        # put all categories in a dict
        all_categories = {}
        for category in categories:
            all_categories[category.id] = category.type

        # if no questions
        if len(current_questions) == 0:
            abort(404)

        # return data to view
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(current_questions),
            'categories': all_categories
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            # get the question
            question = Question.query.filter(Question.id == question_id)\
                .one_or_none()

            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)

            # if no question found abort 404
            if question is None:
                abort(404)

            # delete the question
            question.delete()

            # return success response
            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(questions)
            })

        except:
            # if problem deleting
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def create_search_question():
        # load the request body
        body = request.get_json()

        # load data from body
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        search = body.get('searchTerm', None)

        try:
            if search:
                selection = Question.query.order_by(Question.id)\
                    .filter(Question.question.ilike('%{}%'.format(search)))
                current_questions = paginate_questions(request, selection)

                # return data to view
                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(Question.query.all())
                })
            else:
                # ensure all fields have data
                if new_category is None or new_difficulty is None or \
                        new_answer is None or new_question is None:
                    abort(422)

                # create and insert new question
                question = Question(question=new_question,
                                    answer=new_answer, category=new_category,
                                    difficulty=new_difficulty)
                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                # return data to view
                return jsonify({
                    'success': True,
                    'created': question.id,
                    'questions': current_questions,
                    'total_questions': len(selection)
                })

        except:
            abort(422)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        # get the category by id
        category = Category.query.filter_by(id=category_id).one_or_none()

        # if category isn't found
        if category is None:
            abort(400)

        # get the matching questions
        questions = Question.query.filter(Question.category ==
                                          str(category_id)).all()
        current_questions = paginate_questions(request, questions)

        # return data to view
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'current_catogory': category.type
        })

    @app.route('/quizzes', methods=['POST'])
    def get_questions_quiz():
        # load the request body
        body = request.get_json()

        # abort 400 if category or previous questions or body isn't found
        if body is None or body['previous_questions'] is None \
                or body['quiz_category'] is None:
            abort(400)

        previous_questions = body['previous_questions']
        category = body['quiz_category']

        # if ALL is selected load all questions
        if category['id'] == 0:
            questions = Question.query\
                .filter(Question.id.notin_(previous_questions)).all()
        else:
            # load questions for given category
            questions = Question.query\
                .filter(Question.id.notin_(previous_questions),
                        Question.category == category['id']).all()

        if len(questions) == 0 or questions is None:
            question = None
        else:
            #  get random question
            choice = random.randint(0, len(questions)-1)
            question = questions[choice]

        # return data to view
        return jsonify({
            'success': True,
            'question': question.format() if question is not None else None
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400
    return app
