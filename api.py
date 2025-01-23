from flask import Flask
from flask_restx import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'



db = SQLAlchemy()
#migrate = Migrate(app,db)

db.init_app(app)

cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000/*"}})

class User(db.Model): #Model for the DB
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=True)
    def __repr__(self): #Special test function to output to string
        return '<User %r>' % self.username
    
#TODO Initialise the database and fill with test data

with app.app_context():
    db.create_all()

testUser = User(username='test', email='')

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        print(User.query.all())
        return {'hello': User.query.all()}
        
    

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help='username')
parser.add_argument('password', type=str, required=True, help='password')



@api.route('/register', methods=['POST'])
class postShit(Resource):
    @api.doc(parser=parser)
    def post(username):
        args = parser.parse_args()
        db.session.add(testUser)
        db.session.commit()

        return 'Hello, ' + args['username']
        

#LOGIN:

#GetLoginInfo
#   Get the Post request
#   JSONify it (maybe done when POST is sent)
#   Check if creds correct (Later implement a DB system for this)
#   return a login token

#CheckLoginToken
# TODO IDK how to

#REGISTER:

#Register User
#   Get post data
#   Parse it into different args
#   Check if user already exists???
#   NewUser = User(username=Arg1, etc.)
#   db.session.add(NewUser)
#   db.session.commit()

#ADMIN:

#Check Logs:
#   TODO - implement logging and figure out how its being stored

#USER:

#Change User Details
#   GET:
#       Query the database
#       Parse the user details into JSON
#       Send the JSON to frontend
#       Frontend then parses the JSON to fill the user details boxes
#   POST:
#       Get the JSON (only send the changed bits?)
#       Update the user table with the new info
#       Commit the changes

#Check Orders:
#   TODO

#Check Basket:
#   TODO

#SELLER PAGE:

#Show current products
#   TODO

#Sellers Report
#   TODO

#Add new product
#   TODO

#Edit current products
#   TODO

if __name__ == '__main__':
    app.run(debug=True)