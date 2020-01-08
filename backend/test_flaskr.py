import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from .flaskr import create_app
from .models import db, setup_db, Question, Category


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
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

        """
    TODO
    Write at least one test for each test for successful operation and for 
    expected errors.
    """

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

    def test_delete_question(self):
        res = self.client().delete('/questions/20')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 20).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 20)
        self.assertEqual(question, None)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_add_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

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

    def test_search_with_result_case_insensitive(self):
        res = self.client().post('/questions', json={'searchTerm': 'MAhaL'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)
        self.assertTrue(data['total_matching_questions'])

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category']['id'], 3)
        self.assertEqual(data['current_category']['type'], 'Geography')
        self.assertEqual(len(data['questions']), 3)
        self.assertTrue(data['total_in_category'])



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
