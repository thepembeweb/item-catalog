from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

Base = declarative_base()


# setup Movie genres class
class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id
        }


# setup User class
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    picture = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'email': self.email,
            'picture': self.picture
        }


# setup Movie class
class Movie(Base):
    __tablename__ = 'movies'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(4000))
    rating = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    image_url = Column(String(400), nullable=True)
    genre_id = Column(Integer, ForeignKey('genres.id'))
    genres = relationship(
        'Genre', backref='genre_movies', foreign_keys=[genre_id])
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship(
        'User', backref='user_movies', foreign_keys=[user_id])
    insert_date = Column(DateTime(timezone=True), default=func.now())
    last_update = Column(DateTime(timezone=True), default=func.now())

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'rating': self.rating,
            'duration': self.duration,
            'image_url': self.image_url,
            'genre_id': self.genre_id,
            'user_id': self.user_id,
            'insert_date': self.insert_date,
            'last_update': self.last_update
        }
