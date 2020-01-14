import os
import unittest
import json

from flask_sqlalchemy import SQLAlchemy

from .flaskr import create_app
from .models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'asdf', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # new question for testing purposes
        self.new_question = {
            'question': 'What does the fox say?',
            'answer': 'Ring-ding-ding-ding-dingeringeding',
            'difficulty': 99,
            'category': '5'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            # self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['current_category'], None)

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        self.assertEqual(len(data['categories']), 6)

    def test_get_categories_not_exist(self):
        res = self.client().get('/categories/9000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'The requested URL was not found on '
                                          'the server. If you entered the URL '
                                          'manually please check your '
                                          'spelling and try again.')

    def test_delete_question(self):
        # add test question to be deleted
        test_question = Question(question="test", answer="test", category=1,
                                 difficulty=1)
        test_question.insert()
        test_question_id = test_question.id

        res = self.client().delete(f'/questions/{test_question_id}')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id ==
                                         test_question_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], test_question_id)
        self.assertEqual(question, None)
        self.assertTrue(data['total_questions'])

    def test_delete_question_not_exist(self):
        res = self.client().delete('/questions/9000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'The request was well-formed but '
                                          'was unable to be followed due to '
                                          'semantic errors.')

    def test_add_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_id'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_add_question_invalid_question_field(self):
        res = self.client().post('/questions', json={
            'question': '',
            'answer': 'but question is emtpy!',
            'category': 1,
            'difficulty': 5
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could not '
                                          'understand.')

    def test_add_question_invalid_answer_field(self):
        res = self.client().post('/questions', json={
            'question': 'but answer is empty!',
            'answer': '',
            'category': 1,
            'difficulty': 5
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could not '
                                          'understand.')

    def test_get_specific_question(self):
        res = self.client().get('/questions/17')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question_id'], 17)
        self.assertEqual(data['difficulty'], 3)
        self.assertTrue(data['question'])
        self.assertTrue(data['answer'])
        self.assertEqual(data['category'], 2)

    def test_get_specific_question_not_exist(self):
        res = self.client().get('/questions/9000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'The requested URL was not found on '
                                          'the server. If you entered the URL '
                                          'manually please check your '
                                          'spelling and try again.')

    def test_search_with_result_case_insensitive(self):
        res = self.client().post('/questions', json={'searchTerm': 'MAhaL'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)
        self.assertTrue(data['total_matching_questions'])

    def test_search_with_no_result(self):
        res = self.client().post('/questions', json={
            'searchTerm': "ThIs won'T be FouND"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_matching_questions'], 0)

    def test_search_with_empty_search_term(self):
        # only invalid search term would be an empty search
        res = self.client().post('/questions', json={
            'searchTerm': ''
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could not '
                                          'understand.')

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category']['id'], 3)
        self.assertEqual(data['current_category']['type'], 'Geography')
        self.assertEqual(len(data['questions']), 3)
        self.assertTrue(data['total_in_category'])

    def test_get_questions_by_invalid_or_empty_category(self):
        res = self.client().get('/categories/9000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'The requested URL was not found on '
                                          'the server. If you entered the URL '
                                          'manually please check your '
                                          'spelling and try again.')

    def test_get_trivia_questions_all_categories(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {'id': 0}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_get_trivia_questions_specific_category(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {'id': 3}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 3)

    def test_get_trivia_questions_invalid_body_missing_previous_questions(
            self):
        res = self.client().post('/quizzes', json={
            'quiz_category': {'id': 3}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could not '
                                          'understand.')

    def test_get_trivia_questions_invalid_body_missing_category(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': []
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could not '
                                          'understand.')

    def test_get_trivia_questions_valid_body_invalid_category(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {'id': 9000}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The request was well-formed but was'
                                          ' unable to be followed due to '
                                          'semantic errors.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
