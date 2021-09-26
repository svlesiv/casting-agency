import os
import enum
from datetime import datetime
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
from dotenv import load_dotenv

database_name = os.environ.get("DATA_BASE_NAME")

database_path = "postgresql://{}/{}".format(
            'localhost:5432', database_name)
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    
'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple
    verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    movie = Movie(
        title='First movie',
        release_date=datetime.now()
    )
    movie.insert()
    
    actor = Actor(
        name='First actress',
        age='25',
        gender='female'
    )
    
    actor.insert()
    
class GenderEnum(enum.Enum):
    female = 'female'
    male = 'male'
    
association_table = db.Table('association_table',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True)
    )

# Movies with attributes title and release date
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = Column(String(80), unique=True, nullable=False)
    release_date = db.Column(
        db.DateTime, default=datetime.now())
    actors = db.relationship('Actor', secondary='association_table', backref=db.backref('movies', lazy=True))
    
    def format_movie(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }
        
    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    '''
    update()
        updates a new model into a database
        the model must exist in the database
    '''

    def update(self):
        db.session.commit()
        
    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
   
    
# Actors with attributes name, age and gender
class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    age = Column(db.Integer)
    gender = db.Column(db.Enum(GenderEnum))
    
    def format_actor(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': json.dumps(self.gender, default=lambda x: x.value),
        }
        
    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    '''
    update()
        updates a new model into a database
        the model must exist in the database
    '''

    def update(self):
        db.session.commit()
    
    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()
