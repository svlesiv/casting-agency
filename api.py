from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from database.models import db, db_drop_and_create_all, setup_db, Actor, Movie
from auth.auth import AuthError, requires_auth
from flask_migrate import Migrate


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    # Uncomment the following line on the initial run to setup
    # the required tables in the database
    # db_drop_and_create_all()

    CORS(app, resources={r"/*": {"origins": "*"}})

    migrate = Migrate(app, db)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    '''
    Uncommenting the following line to initialize the database
    !! WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! THIS MUST BE UNCOMMENTED ON FIRST RUN
    !! Running this funciton will add one
    '''
    # db_drop_and_create_all()

    @app.route('/')
    def index():
        return 'Hello'

    '''
    GET /actors
    '''
    @app.route('/actors')
    @requires_auth("get:actors")
    def get_actor(jwt):
        actors = Actor.query.order_by(Actor.id).all()

        if not actors:
            abort(404)

        return jsonify({
            "success": True,
            "actors": [actor.format_actor() for actor in actors]
        }), 200

    '''
    GET /movies
    '''
    @app.route('/movies')
    @requires_auth("get:movies")
    def get_movie(jwt):
        movies = Movie.query.order_by(Movie.id).all()

        if not movies:
            abort(404)

        return jsonify({
            "success": True,
            "movies": [movie.format_movie() for movie in movies]
        }), 200

    '''
    POST /actors
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth("post:actors")
    def post_actor(jwt):
        body = request.get_json()
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')
        new_actor = Actor(name=name, age=age, gender=gender)

        try:
            new_actor.insert()
            return jsonify({
                "success": True,
                "actor": [new_actor.format_actor()]
            }), 200

        except Exception as err:
            print(err)
            abort(422)

    '''
    POST /movies
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth("post:movies")
    def post_movie(jwt):
        body = request.get_json()
        title = body.get('title')
        release_date = body.get('release_date')
        new_movie = Movie(title=title, release_date=release_date)

        print(new_movie.format_movie())

        try:
            new_movie.insert()
            return jsonify({
                "success": True,
                "movie": [new_movie.format_movie()]
            }), 200

        except Exception as err:
            print(err)
            abort(422)

    '''
    PATCH /actors/<id>
    '''
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth("patch:actors")
    def update_actor(jwt, actor_id):
        actor = Actor.query.get(actor_id)

        if not actor:
            abort(404)

        body = request.get_json()
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        if name:
            actor.name = name

        if age:
            actor.age = age

        if gender:
            actor.age = age

        whitelistedBody = {k: body[k] for k in
                           ['name', 'age', 'gender'] if k in body}

        if len(whitelistedBody) != len(body):
            abort(422)

        try:
            actor.update()

            return jsonify({
                "success": True,
                "actors": [actor.format_actor()]
            }), 200

        except Exception as err:
            print(err)
            abort(422)

    '''
    PATCH /movies/<id>
    '''
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth("patch:movies")
    def update_movie(jwt, movie_id):
        movie = Movie.query.get(movie_id)

        if not movie:
            abort(404)

        body = request.get_json()
        title = body.get('title')
        release_date = body.get('release_date')

        if title:
            movie.title = title

        if release_date:
            movie.release_date = release_date

        whitelistedBody = {k: body[k] for k in
                           ['title', 'release_date'] if k in body}

        if len(whitelistedBody) != len(body):
            abort(422)

        try:
            movie.update()

            return jsonify({
                "success": True,
                "movies": [movie.format_movie()]
            }), 200

        except Exception as err:
            print(err)
            abort(422)

    '''
    DELETE /actors/<id>
    '''
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth("delete:actors")
    def delete_actor(jwt, actor_id):
        try:
            actor = Actor.query.get(actor_id)

            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'delete': actor_id,
            }), 200

        except Exception as err:
            print(err)
            abort(422)

    '''
    DELETE /movies/<id>
    '''
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth("delete:movies")
    def delete_movie(jwt, movie_id):
        try:
            movie = Movie.query.get(movie_id)

            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'delete': movie_id,
            }), 200

        except Exception as err:
            print(err)
            abort(422)

    '''
    Error Handling
    '''
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "forbidden"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def invalid_method(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "invalid method"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server error"
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
