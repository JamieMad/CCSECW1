from flask import Flask, request, jsonify
from flask_restx import Resource, Api, reqparse, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from dataclasses import dataclass

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'



db = SQLAlchemy()
#migrate = Migrate(app,db)

db.init_app(app)

cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000/*"}})

@dataclass #Used for verifying data and documentation
class User(db.Model): #Model for the DB

    id: int #sets the expected data types for when JSONified
    username: str
    email: str

    __tablename__ = 'Users' #Set tablename
    id: Mapped[int] = mapped_column(unique=True, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self): #Special test function to output to string
        return '<User %r>' % self.username

@dataclass
class Products(db.Model):
    id : int
    name : str
    description : str
    numberSold : int
    cost : int #Stored in pence
    owner : int

    __tablename__ = 'Products'
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    numberSold: Mapped[int] = mapped_column(nullable=False)
    cost: Mapped[int] = mapped_column(nullable=False)
    owner: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)

@dataclass
class Orders(db.Model):
    id : int
    orderFulfilled : bool
    customerID : int
    sellerID : int

    __tablename__ = 'Orders'
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    orderFulfilled: Mapped[bool] = mapped_column(nullable=False)
    customerID: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)
    sellerID: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)

@dataclass
class ItemInOrder(db.Model):
    orderID : int
    productID : int
    quantity : int

    __tablename__ = 'item_in_order'
    orderID : Mapped[int] = mapped_column(primary_key=True, nullable=False)
    productID : Mapped[int] = mapped_column(primary_key=True, nullable=False)
    quantity : Mapped[int] = mapped_column(nullable=False)

with app.app_context():  #Initialise the database and fill with test data
    db.drop_all() #TODO remove
    db.create_all()

testUser = User(username='test', email='')

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        print(User.query.all())
        #return {'hello': User.query.all()}
        


parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help='username')
parser.add_argument('password', type=str, required=True, help='password')



@api.route('/postshit', methods=['POST'])
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
#   Check if user already exists??? TODO
#   NewUser = User(username=Arg1, etc.)
#   db.session.add(NewUser)
#   db.session.commit()

RegisterModel = api.model('RegisterModel', {
    'username': fields.String,
    'password': fields.String(required=True)
})

@api.route('/register', methods=['POST'])
class register(Resource):
    @api.expect(RegisterModel, validate=True) #When validating check errors aren't returned to users TODO
    def post(username):
        data = request.get_json()
        newUser = User(username=data['username'],email=data['password'])
        db.session.add(newUser)
        db.session.commit()
        result = db.session.execute(db.select(User))
        print(result.all())
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

@api.route('/userdetails/<int:id>', methods=['GET','POST']) #TODO somehow need to protect this
class getUserDetails(Resource):
    def get(self, id):
        userDetails = User.query.filter_by(id=id).all()
        return jsonify(userDetails)
        
@api.route('/getallusers', methods=['GET']) #TODO remove this
class getUserDetails(Resource):
    def get(self):
        userDetails = User.query.all()
        return jsonify(userDetails)

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