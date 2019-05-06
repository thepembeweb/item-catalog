from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Genre, Movie

engine = create_engine('sqlite:///moviezone.db')
Base.metadata.create_all(engine)

# setup DB session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# default Movie genres
GENRES = [
    'Action',
    'Adventure',
    'Animation',
    'Biography',
    'Comedy',
    'Crime',
    'Drama',
    'Family',
    'Fantasy',
    'History',
    'Horror',
    'Music',
    'Musical',
    'Mystery',
    'Romance',
    'Sci-Fi',
    'Sport',
    'Thriller',
    'War',
    'Western'
]

# add Movie genres
def addGenres():
    for genre in GENRES:
        session.add(Genre(name=genre))
    session.commit()


if __name__ == '__main__':
    addGenres()
