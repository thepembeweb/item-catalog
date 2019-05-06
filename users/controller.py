import dicttoxml
from flask import session as login_session
from flask import Blueprint
from flask import request
from flask import jsonify
from database import db_session
from models import User

users = Blueprint('users', __name__)


# setup show Users route
@users.route('/users')
def showUsers():
    xml_format = request.args.get('xml')
    users = db_session.query(User).all()
    serialized_result = [i.serialize for i in users]

    if (xml_format == 'true' or xml_format == 'TRUE'):
        xml_output = dicttoxml.dicttoxml(serialized_result)
        return xml_output, 200, {'Content-Type': 'text/xml; charset=utf-8'}
    else:
        return jsonify(collection=serialized_result)


# setup show User route
@users.route('/users/<int:user_id>', methods=['GET'])
def showUser(user_id):
    xml_format = request.args.get('xml')
    users = db_session.query(User).filter(
        User.id == user_id).all()
    serialized_result = [i.serialize for i in users]

    if (xml_format == 'true' or xml_format == 'TRUE'):
        xml_output = dicttoxml.dicttoxml(serialized_result)
        return xml_output, 200, {'Content-Type': 'text/xml; charset=utf-8'}
    else:
        return jsonify(collection=serialized_result)
