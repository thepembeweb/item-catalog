import random
import string
import httplib2
import json
import requests
from flask import render_template, redirect, url_for
from flask import session as login_session
from flask import Blueprint
from flask import request
from flask import jsonify
from database import db_session
from models import User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

auth = Blueprint('auth', __name__, template_folder='templates')

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Moviezone"


# creates new user
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    db_session.add(newUser)
    db_session.commit()
    return newUser.id


# retrieves user info
def getUserInfo(user_id):
    user = db_session.query(User).filter_by(id=user_id).one()
    return user


# retrieves user Id
def getUserID(email):
    try:
        user = db_session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# generates user token
def generateToken():
    state = ''.join(random.choice(string.ascii_lowercase + string.digits)
                    for x in xrange(32))
    return state


# setup home route
@auth.route('/')
def home():
    """Here we register the route for the homepage"""
    try:
        login_session['state'] = generateToken()
        return render_template(
            'index.html',
            session=login_session,
            state=login_session['state']
        )
    except TemplateNotFound:
        abort(404)


# setup login route
@auth.route('/auth/login', methods=['GET'])
def showLoginPage():
    if 'username' not in login_session:
        login_session['state'] = generateToken()
        return render_template('auth.html', state=login_session['state'])
    else:
        return redirect('/')


# setup google connect route
@auth.route('/auth/gconnect', methods=['POST'])
def gconnect():
    if request.headers.get('moviezone-token') != login_session['state']:
        resp = jsonify(error=['You are not allowed to make such request.'])
        resp.status_code = 401
        return resp

    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError, e:
        resp = jsonify(error=[e.message])
        resp.status_code = 401
        return resp

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        resp = jsonify(error=[result.get('error')])
        resp.status_code = 500
        return resp

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        resp = jsonify(error=["Token's user ID doesn't match given user ID."])
        resp.status_code = 401
        return resp

    if result['issued_to'] != CLIENT_ID:
        resp = jsonify(error=["Token's client ID does not match app's."])
        resp.status_code = 401
        return resp

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        resp = jsonify(success=['Current user is already connected.'])
        resp.status_code = 401
        return resp

    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    login_session['provider'] = 'google'

    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    return jsonify(success=['Login Successful'], data=data)


# setup clear session route
@auth.route('/clearSession')
def clearSession():
    login_session.clear()
    return redirect(url_for('.home'))


# setup google disconnect route
@auth.route('/auth/gdisconnect')
def gdisconnect():
    credentials = login_session.get('credentials')
    if credentials is None:
        return render_template(
            'errorpage.html',
            error='Current user not connected.',
            status=401
        )
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print result

    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']

    else:
        return render_template(
            'errorpage.html',
            error='Failed to revoke token for given user.',
            status=400
        )


# setup disconnect route
@auth.route('/auth/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        return redirect(url_for('.home'))
    else:
        return render_template(
            'errorpage.html',
            error='You are not logged in.',
            status=401
        )
