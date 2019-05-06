from flask import Flask, render_template
from database import init_db
from movies.controller import movies
from genres.controller import genres
from auth.controller import auth
from users.controller import users

init_db()
app = Flask(__name__)
app.secret_key = 'P2Bc51x/6qL p~HMQ!waZ]GPU/,?JS'

# register blueprint
app.register_blueprint(movies)
app.register_blueprint(genres)
app.register_blueprint(auth)
app.register_blueprint(users)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
