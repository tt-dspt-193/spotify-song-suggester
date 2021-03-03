"""Flask Login Example and instagram fallowing find"""

from flask import Flask, url_for, render_template, request, redirect, session, jsonify, Response
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spotify.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Users(db.Model):
    """ Create user table"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    song = db.relationship('Songs', backref="users", lazy='select')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {'id': self.id, 'username': self.username,
                'password': self.password}
        # this method we are defining will convert our output to json


    def get_all_users():
        '''function to get all users in our database'''
        return [Users.json(user) for user in Users.query.all()]

    def get_user(_id):
        '''function to get user using the id of the user as parameter'''
        return [Users.json(Users.query.filter_by(id=_id).first())]

    def add_user(username, password):
        '''function to add user to database using username, password
        as parameters'''
        # creating an instance of our User constructor
        new_user = Users(username=username, password=password)
        db.session.add(new_user)  # add new user to database session
        db.session.commit()  # commit changes to session

    def update_user(_id,username, password):
        '''function to update the details of a user using the id, username,
        password as parameters'''
        user_to_update = Users.query.filter_by(id=_id).first()
        user_to_update.username = username
        user_to_update.password = password
        db.session.commit()

    def delete_user(_id):
        '''function to delete a user from our database using
           the id of the user as a parameter'''
        Users.query.filter_by(id=_id).delete()
        # filter user by id and delete
        db.session.commit()  # commiting the new change to our database

class Songs(db.Model):
    """ Create song table"""
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    acousticness = db.Column(db.Float())
    artists = db.Column(db.String())
    danceability = db.Column(db.Float())
    name = db.Column(db.String())
    popularity = db.Column(db.Integer())
    favorite = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
       "users.id"), nullable=False)
   

    def __init__(self, acousticness, artists, danceability, name, popularity, favorite):
        self.acousticness = acousticness
        self.artists = artists
        self.danceability = danceability
        self.name = name
        self.popularity = popularity
        self.favorite = favorite    

    def json(self):
        return {'id': self.id, 'acousticness': self.acousticness,
                'artists': self.artists, 'danceability': self.danceability,
                'name': self.name, 'popularity': self.popularity, 'favorite': self.favorite, 'user_id': self.user_id}
        # this method we are defining will convert our output to json

    def get_all_songs():
        '''function to get all songs in our database'''
        return [Songs.json(song) for song in Songs.query.all()]

    def get_song(_id):
        '''function to get song using the id of the song as parameter'''
        return [Songs.json(Songs.query.filter_by(id=_id).first())]

    def add_song(acousticness, artists, danceability, name, popularity, favorite, user_id):
        '''function to add song to database using acousticness, artists, danceability, name, popularity
        as parameters'''
        # creating an instance of our Song constructor
        new_song = Songs(acousticness=acousticness, artists=artists, danceability=danceability, name=name, popularity=popularity, favorite=favorite)
        user = Users.query.filter_by(id=user_id).first()
        user.song.append(new_song)
        db.session.add(new_song)  # add new song to database session
        # db.session.commit()  # commit changes to session

    def update_song(_id, acousticness, artists, danceability, name, popularity, favorite):
        '''function to update the details of a song using the acousticness, artists, danceability, name, popularity,
         as parameters'''
        song_to_update = Songs.query.filter_by(id=_id).first()
        song_to_update.acousticness = acousticness
        song_to_update.artists = artists
        song_to_update.danceability = danceability
        song_to_update.name = name
        song_to_update.popularity = popularity
        song_to_update.favorite = favorite
        db.session.commit()

    def delete_song(_id):
        '''function to delete a song from our database using
           the id of the song as a parameter'''
        Songs.query.filter_by(id=_id).delete()
        # filter user by id and delete
        db.session.commit()  # commiting the new change to our database


#route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    '''Function to get all the users in the database'''
    return jsonify({'Users': Users.get_all_users()})

#route to get user by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    return_value = Users.get_user(id)
    return jsonify(return_value)

#route to add a new user
@app.route('/users', methods=['POST'])
def add_user():
    '''Function to add new user to our database'''
    request_data = request.get_json(force=True)  # getting data from client
    Users.add_user(request_data["username"], request_data["password"])
    response = Response("User added", 201, mimetype='application/json')
    # return str("DOne")
    return response

# route to update user with PUT method
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    '''Function to edit user in our database using user id'''
    request_data = request.get_json()
    Users.update_user(id, request_data['username'], request_data['password'])                                     
    response = Response("User Updated", status=200, mimetype='application/json')
    return response

# route to delete user using the DELETE method
@app.route('/users/<int:id>', methods=['DELETE'])
def remove_user(id):
    '''Function to delete user from our database'''
    Users.delete_user(id)
    response = Response("User Deleted", status=200, mimetype='application/json')
    return response


#route to get all songs
@app.route('/songs', methods=['GET'])
def get_songs():
    '''Function to get all the songs in the database'''
    return jsonify({'Songs': Songs.get_all_songs()})

#route to get song by id
@app.route('/songs/<int:id>', methods=['GET'])
def get_song_by_id(id):
    return_value = Songs.get_song(id)
    return jsonify(return_value)

#route to add a new song
@app.route('/songs', methods=['POST'])
def add_song():
    '''Function to add new song to our database'''
    request_data = request.get_json(force=True)  # getting data from client
    # user_id = request_data["userId"]
    
    # print(request_data)
    Songs.add_song(request_data["acousticness"], request_data["artists"], request_data["danceability"], request_data["name"], request_data["popularity"], request_data["favorite"], request_data["userId"])
    db.session.commit()
    # response = Response("Song added", 201, mimetype='application/json')
    return str("DOne")
    # return response

# route to update song with PUT method
@app.route('/songs/<int:id>', methods=['PUT'])
def update_song(id):
    '''Function to edit song in our database using song id'''
    request_data = request.get_json()
    Songs.update_song(id, request_data["acousticness"], request_data["artists"], request_data["danceability"], request_data["name"], request_data["popularity"], request_data["favorite"])                                     
    response = Response("Song Updated", status=200, mimetype='application/json')
    return response

# route to delete song using the DELETE method
@app.route('/songs/<int:id>', methods=['DELETE'])
def remove_song(id):
    '''Function to delete song from our database'''
    Songs.delete_song(id)
    response = Response("Song Deleted", status=200, mimetype='application/json')
    return response



# @app.cli.command()
# def createsong():
#     # click.echo('Init the db')
#     # db.create_all()

#     # Create a test song
#     new_song = Songs("0.9", "Mamie", "0.5", "Keep", "23")
#     db.session.add(new_song)
#     print(new_song.json())
#     # db.session.commit()
#     print("[Songs.query.filter_by(id=1).first().artists]")

# @app.before_first_request
# def create_tables():
#     db.create_all()

# if __name__ == "__main__":
#     # db.create_all()
#     app.run(debug=True)


@app.route('/', methods=['GET', 'POST'])
def home():
    """ Session control"""
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        if request.method == 'POST':
            username = getname(request.form['username'])
            return render_template('index.html', data=Users.query.filter_by(username=name).first())
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        try:
            data = Users.query.filter_by(username=name, password=passw).first()
            if data is not None:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return 'Dont Login'
        except:
            return "Dont Login"


@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Register Form"""
    if request.method == 'POST':
        new_user = Users(
            username=request.form['username'],
            password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')
    return render_template('register.html')


@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))

@app.route("/hello")
def hello():
    return str("Hello")

# @app.cli.command()
# def initdb():
#     db.create_all()

#     # Create a test user
#     new_user = User('Bryt', 'aaaaaaaa')
#     db.session.add(new_user)
#     db.session.commit()


# @app.cli.command()
# def initdbs():
#     """Populates database with data."""
#     db.drop_all()
#     db.create_all()

#     s = Songs(
#         acousticness= 0.5, artists ='Bob Marley', danceability=5.5, name='No woman no cry',
#         popularity=70, favorite=True
#     )
#     db.session.add(s)

#     u= Users(username='kwame', password='kjhghh')
#     db.session.add(u)
#     u.song.append(s)
#     db.session.commit()

if __name__ == '__main__':
    app.debug = True
    # db.create_all()
    # app.secret_key = "123"
    app.run(host='0.0.0.0')


# def init_db():
#     db.create_all()

#     # Create a test user
#     new_user = User('Bryt', 'aaaaaaaa')
#     db.session.add(new_user)
#     db.session.commit()


if __name__ == '__main__':
    init_db()