import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from ..models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # set up CORS
    CORS(app, resource={r'/api/*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PUT,PATCH,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.all()
            if len(categories) == 0:
                abort(404)
            return jsonify({
                'success': True,
                'categories': {
                    category.id: category.type for category in categories
                }
            })

        except Exception as error:
            raise error

        finally:
            db.session.close()

    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
            questions = Question.query.all()
            paginated_questions = paginate_questions(request, questions)
            categories = [category.format() for category in
                          Category.query.all()]

            if questions is None:
                abort(404)
            return jsonify({
                'success': True,
                'questions': paginated_questions,
                'total_questions': len(Question.query.all()),
                'current_category': None,
                'categories': categories
             })

        except Exception as error:
            raise error

        finally:
            db.session.close()

    @app.route('/questions/<int:question_id>', methods=['GET'])
    def get_specific_question(question_id):
        try:
            question = Question.query.filter(Question.id ==
                                             question_id).one_or_none()

            if question is None:
                abort(404)

            return jsonify({
                'success': True,
                'question_id': question_id,
                'question': question.question,
                'answer': question.answer,
                'category': question.category,
                'difficulty': question.difficulty
             })

        except Exception as error:
            raise error

        finally:
            db.session.close()

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id ==
                                             question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })

        except Exception as error:
            raise error

        finally:
            db.session.close()

    @app.route('/questions', methods=['POST'])
    def add_or_search_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)
        search = body.get('searchTerm', None)

        try:
            if search is not None:
                if body['searchTerm'] == '':
                    abort(400)
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike(f'%{search}%'))
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    'body': body,
                    'success': True,
                    'questions': current_questions,
                    'total_matching_questions': len(selection.all())
                }), 200

            else:
                if len(new_question) == 0 or len(new_answer) == 0:
                    abort(400)
                question = Question(question=new_question,
                                    answer=new_answer,
                                    difficulty=new_difficulty,
                                    category=new_category)
                question.insert()

                current_questions = paginate_questions(request, Question.query.
                                                       order_by(Question.id).
                                                       all())

                return jsonify({
                    'body': body,
                    'success': True,
                    'created_id': question.id,
                    'new_question': question.format(),
                    'questions': current_questions,
                    'total_questions': len(Question.query.all())
                }), 201

        except Exception as error:
            raise error

        finally:
            db.session.close()

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            category = Category.query.get(category_id)
            questions = Question.query.filter(
                Question.category == category_id).all()

            if not questions:
                abort(404)

            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'total_questions': len(Question.query.all()),
                'total_in_category': len(questions),
                'current_category': category.format()
            })

        except Exception as error:
            raise error

        finally:
            db.session.close()

    @app.route('/quizzes', methods=['POST'])
    def play_trivia():
        try:
            body = request.get_json()

            valid_categories = [0, 1, 2, 3, 4, 5, 6]
            if 'quiz_category' not in body or 'previous_questions' not in body:
                abort(400)
            elif int(body.get('quiz_category')['id']) not in valid_categories:
                abort(422)

            questions = [question.format() for question in
                         Question.query.filter(Question.id.notin_(
                             body.get('previous_questions'))).all()]

            if body.get('quiz_category')['id'] != 0:
                questions = [question.format() for question in
                             Question.query.filter_by(category=body.get(
                                 'quiz_category')['id']).filter(
                                 Question.id.notin_(body.get(
                                     'previous_questions'))).all()]

            if questions:
                next_question = random.choice(questions)
            else:
                next_question = None

            return jsonify({
                'success': True,
                'question': next_question
            })

        except Exception as error:
            raise error

        finally:
            db.session.close()

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": error.description
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": error.description
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": error.description
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": error.description
        }), 405

    return app


if __name__ == "__main__":
    create_app()
