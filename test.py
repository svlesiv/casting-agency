from datetime import datetime
import os
import unittest
import json
from flask import Flask
import json
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from database.models import setup_db, Movie, Actor
from api import create_app

# create a database file: pg_dump dbname > dbexport.pgsql
# create a database for testing: createdb casting_agency_database_test
# psql -f casting_agency_database.psql -d casting_agency_database_test


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.assistant_token = os.environ.get('ASSISTANT')
        self.director_token = os.environ.get('DIRECTOR')
        self.producer_token = os.environ.get('PRODUCER')

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = os.environ.get('TEST_DATA_BASE_NAME')
        self.database_path = os.environ.get('DATABASE_URL',
                                            "postgresql://{}/{}".format(
                                                'localhost:5432',
                                                self.database_name))
        if self.database_path.startswith("postgres://"):
            self.database_path = self.database_path.replace(
                "postgres://", "postgresql://", 1)
        setup_db(self.app, self.database_path)
        CORS(self.app, resources={r"/*": {"origins": "*"}})

        self.new_actor = {
            'name': 'New Actor - 4',
            'age': 25,
            'gender': 'female'
        }

        self.new_actor_malformed = {
            'error_name': 'fail',
        }

        self.update_actor = {
            'name': 'New Actor - 5',
        }

        self.update_actor_malformed = {
            'random_field': 'fail',
        }

        self.new_movie = {
            'title': 'New Movie - 5',
            'release_date': datetime.now(),
        }

        self.new_movie_malformed = {
            'error_title': 'fail',
            'release_date': datetime.now(),
        }

        self.update_movie = {
            'title': 'Awesome 1',
        }

        self.update_movie_malformed = {
            'error_title': 'fail',
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    ############################################
    # GET '/actors'
    ############################################

    def test_get_actors_assistant(self):
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_actors_director(self):
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_actors_producer(self):
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_actors_no_token(self):
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 401)

    ############################################
    # GET '/movies'
    ############################################

    def test_get_movies_assistant(self):
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_movies_director(self):
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_movies_producer(self):
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_movies_no_token(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 401)

    ############################################
    # POST '/actors'
    ############################################

    def test_create_new_actor_assistant_error(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers={
                                     'Authorization':
                                         "Bearer {}".format(
                                             self.assistant_token)
                                 })
        self.assertEqual(res.status_code, 403)

    def test_create_new_actor_director(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers={
                                     'Authorization':
                                         "Bearer {}".format(
                                             self.director_token)
                                 })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_create_new_actor_director_error(self):
        res = self.client().post('/actors', json=self.new_actor_malformed,
                                 headers={
                                     'Authorization':
                                         "Bearer {}".format(
                                             self.director_token)
                                 })
        self.assertEqual(res.status_code, 422)

    def test_create_new_actor_producer(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers={
                                     'Authorization':
                                         "Bearer {}".format(
                                             self.producer_token)
                                 })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_create_new_actor_producer_error(self):
        res = self.client().post('/actors', json=self.new_actor_malformed,
                                 headers={
                                     'Authorization':
                                         "Bearer {}".format(
                                             self.producer_token)
                                 })
        self.assertEqual(res.status_code, 422)

    ############################################
    # POST '/movies'
    ############################################

    def test_create_new_movie_assistant_error(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers={
                                     'Authorization':
                                         "Bearer {}".format(
                                             self.assistant_token)
                                 })
        self.assertEqual(res.status_code, 403)

    def test_create_new_movie_director_error(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers={
                                     'Authorization':
                                         "Bearer {}".format(
                                             self.director_token)
                                 })
        self.assertEqual(res.status_code, 403)

    def test_create_new_movie_producer(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers={
                                     'Authorization':
                                         "Bearer {}".format(
                                             self.producer_token)
                                 })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_create_new_movie_producer_error(self):
        res = self.client().post('/movies', json=self.new_movie_malformed,
                                 headers={
                                     'Authorization':
                                         "Bearer {}".format(
                                             self.producer_token)
                                 })
        self.assertEqual(res.status_code, 422)

    ############################################
    # PATCH '/actors/<id>'
    ############################################

    def test_update_actor_assistant_error(self):
        res = self.client().patch('/actors/6', json=self.update_actor,
                                  headers={
                                      'Authorization':
                                          "Bearer {}".format(
                                              self.assistant_token)
                                  })
        self.assertEqual(res.status_code, 403)

    def test_update_actor_director(self):
        res = self.client().patch('/actors/6', json=self.update_actor,
                                  headers={
                                      'Authorization':
                                          "Bearer {}".format(
                                              self.director_token)
                                  })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_update_actor_director_error(self):
        res = self.client().patch('/actors/6',
                                  json=self.update_actor_malformed,
                                  headers={
                                      'Authorization':
                                          "Bearer {}".format(
                                              self.director_token)
                                  })
        self.assertEqual(res.status_code, 422)

    def test_update_actor_producer(self):
        res = self.client().patch('/actors/6', json=self.update_actor,
                                  headers={
                                      'Authorization':
                                          "Bearer {}".format(
                                              self.producer_token)
                                  })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_update_actor_producer_error(self):
        res = self.client().patch('/actors/6',
                                  json=self.update_actor_malformed,
                                  headers={
                                      'Authorization':
                                          "Bearer {}".format(
                                              self.producer_token)
                                  })
        self.assertEqual(res.status_code, 422)

    ############################################
    # PATCH '/movies/<id>'
    ############################################

    def test_update_movie_assistant_error(self):
        res = self.client().patch('/movies/1', json=self.update_movie,
                                  headers={
                                      'Authorization':
                                          "Bearer {}".format(
                                              self.assistant_token)
                                  })
        self.assertEqual(res.status_code, 403)

    def test_update_movie_director(self):
        res = self.client().patch('/movies/1', json=self.update_movie,
                                  headers={
                                      'Authorization':
                                          "Bearer {}".format(
                                              self.director_token)
                                  })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_update_movie_director_error(self):
        res = self.client().patch('/movies/1',
                                  json=self.update_movie_malformed,
                                  headers={
                                      'Authorization':
                                          "Bearer {}".format(
                                              self.director_token)
                                  })
        self.assertEqual(res.status_code, 422)

    def test_update_movie_producer(self):
        res = self.client().patch('/movies/1', json=self.update_movie,
                                  headers={
                                      'Authorization':
                                          "Bearer {}".format(
                                              self.producer_token)
                                  })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_update_movie_producer_error(self):
        res = self.client().patch('/movies/1',
                                  json=self.update_movie_malformed,
                                  headers={
                                      'Authorization':
                                          "Bearer {}".format(
                                              self.producer_token)
                                  })
        self.assertEqual(res.status_code, 422)

    ############################################
    # DELETE '/actors/<id>'
    ############################################

    def test_delete_actor_assistant_error(self):
        res = self.client().delete('/actors/10', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        self.assertEqual(res.status_code, 403)

    def test_delete_actor_director(self):
        res = self.client().delete('/actors/11', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'], 10)

    def test_delete_actor_director_error(self):
        res = self.client().delete('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })

        self.assertEqual(res.status_code, 422)

    def test_delete_actor_producer(self):
        res = self.client().delete('/actors/13', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'], 13)

    def test_delete_actor_producer_error(self):
        res = self.client().delete('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })

        self.assertEqual(res.status_code, 422)

    ############################################
    # DELETE '/movies/<id>'
    ############################################

    def test_delete_movie_assistant_error(self):
        res = self.client().delete('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        self.assertEqual(res.status_code, 403)

    def test_delete_actor_director_error(self):
        res = self.client().delete('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })

        self.assertEqual(res.status_code, 403)

    def test_delete_movie_producer(self):
        res = self.client().delete('/movies/13', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'], 13)

    def test_delete_movie_producer_error(self):
        res = self.client().delete('/movies/2', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })

        self.assertEqual(res.status_code, 422)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
