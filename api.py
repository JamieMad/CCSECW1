from flask import Flask
from flask_restx import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'

db = SQLAlchemy(app)
migrate = Migrate(app,db)

class User(db.Model): #Model for the DB
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    def __repr__(self): #Special test function to output to string
        return '<User %r>' % self.username
    
#TODO Initialise the database and fill with test data

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        print(User.query.all())
        return {'hello': User.query.all()}
        
    

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, location='form', help='var 1')

@api.route('/post', methods=['POST'])
class postShit(Resource):
    @api.doc(parser=parser)
    def post(username):
        args = parser.parse_args()
        return 'Hello, ' + args['username']
        
        
    
#GetLoginInfo
#   Get the Post request
#   JSONify it (maybe done when POST is sent)
#   Check if creds correct (Later implement a DB system for this)
#   return a login token

#CheckLoginToken
# TODO IDK how to

#


if __name__ == '__main__':
    app.run(debug=True)