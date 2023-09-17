from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_graphql import GraphQLView
import time 
app = Flask(__name__)
app.debug = True
app.app_context().push()
t, token = 0, 'invalid'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/graphql_database'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
app.config['SECRET_KEY'] = 'test_key'
db = SQLAlchemy(app)
db.create_all() # Creates Tables in SQL 
##########

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    books = db.relationship('Book', backref='author')

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '' % self.id

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '' % self.title % self.description % self.year % self.author_id
##########

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
# Schema Objects
class BookObject(SQLAlchemyObjectType):
   class Meta:
       model = Book
       interfaces = (graphene.relay.Node, )

class UserObject(SQLAlchemyObjectType):
   class Meta:
       model = User
       interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_books = SQLAlchemyConnectionField(BookObject)
    all_users = SQLAlchemyConnectionField(UserObject)

schema = graphene.Schema(query=Query)

def auth_required(fn):
    def wrapper(*args, **kwargs):
        session = request.headers.get('AUTH-HEADER')
        elapsed_time = time.perf_counter() - t
        print(t)
        print(elapsed_time)
        if token != 'invalid' and session == token and elapsed_time < 60: 
            return fn(*args, **kwargs) # Check Credentials 
        else: return jsonify({'message':'Failed'}), 401      # Incorrect Keys
    return wrapper

def graphql_view():
    view =GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True # for having the GraphiQL interface
)
    return auth_required(view)


######




@app.route('/')
def index(): return 'Hello World'

@app.route('/token')
def generate_token():
    t = time.perf_counter()  # reset counter, to accept new hash token
    token = str(hash(t))
    return jsonify({'AUTH-HEADER':token})
# Routes
app.add_url_rule(
    '/graphql-Auth',
    view_func = graphql_view()
)

if __name__ == '__main__':
    app.run(host = "0.0.0.0")

# commands:
# pip install flask flask-graphql flask-migrate sqlalchemy graphene graphene-sqlalchemy psycopg2-binary