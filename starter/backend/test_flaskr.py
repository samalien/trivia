import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        #self.database_name = "trivia_test"
        #self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_name = "trivia"
        self.database_path = "postgresql://{}/{}".format('samali:alien@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question' : 'How many players does a football team consist of?',
            'answer' : '11',
            'category' : '6',
            'difficulty' : 1
        }
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res=self.client().get('/categories')
        data=json.loads(res.data)

        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])

    def test_get_questions(self):
        res=self.client().get('/questions')
        data=json.loads(res.data)

        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    # def test_delete_specific_question(self):
    #     res = self.client().delete('/questions/22')
    #     data=json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'],True)
    #     self.assertEqual(data['deleted'],22)
    #     self.assertTrue(data['total_questions'])

    def test_404_if_question_does_not_exist(self):
        res=self.client().delete('/question/2020')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Resource not found')

    def test_create_question(self):
        res=self.client().post('/questions', json=self.new_question)
        data=json.loads(res.data)
        pass

    def test_get_question_search_with_results(self):
        res=self.client().post('/questions',json={'searchTerm':'title'})
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(len(data['questions']),2)
        self.assertTrue(data['total_questions'])

    def test_get_question_search_without_results(self):
        res=self.client().post('/questions', json={'searchTerm':'helloxgxgxgxgx'})
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(len(data['questions']),0)
        self.assertTrue(data['total_questions'])

    def test_get_question_by_category(self):
        res=self.client().get('/categories/5/questions')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_catogory'],'Entertainment')
    def test_400_category_does_not_exist(self):
        res=self.client().get('categories/500/questions')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'bad request')

    def test_play_quiz_success(self):
        res = self.client().post('/quizzes',json={'previous_questions': [11, 66],'quiz_category': {'type': 'Sports', 'id': '6'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], '6')
        self.assertNotEqual(data['question']['id'], 66)

    def test_play_quiz_fails(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()