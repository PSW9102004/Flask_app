# app.py

from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer <token>"'
    }
}


api = Api(app, version='1.0', title='User API', doc='/docs', authorizations=authorizations, security='Bearer')
ns = api.namespace('users', description='User operations')

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# API models
user_model = api.model('User', {
    'id': fields.Integer(readonly=True),
    'username': fields.String(required=True),
    'email': fields.String(required=True)
})


# Parser for login
login_parser = api.parser()
login_parser.add_argument('username', required=True, help='User name')
login_parser.add_argument('password', required=True, help='Password')

@api.route('/login')
class Login(Resource):
    @api.expect(login_parser)
    def post(self):
        args = login_parser.parse_args()
        # Simplified: accept any credentials for demo
        token = create_access_token(identity=args['username'])
        return {'access_token': token}, 200

@ns.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    @jwt_required()
    def get(self):
        return User.query.all()

    @api.doc('create_user')
    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    @jwt_required()
    def post(self):
        data = api.payload
        user = User(username=data['username'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        return user, 201

@ns.route('/<int:id>')
@api.response(404, 'User not found')
class UserResource(Resource):
    @api.marshal_with(user_model)
    @jwt_required()
    def get(self, id):
        user = User.query.get_or_404(id)
        return user

    @api.response(204, 'User deleted')
    @jwt_required()
    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

if __name__ == '__main__':
    # Create tables and run the app
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
