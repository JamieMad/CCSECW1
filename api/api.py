from flask import Flask, request, jsonify, Blueprint, url_for
from flask_restx import Resource, Api, reqparse, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from dataclasses import dataclass
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt_identity, jwt_required, current_user, set_access_cookies, set_refresh_cookies, get_jwt, verify_jwt_in_request
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

from datetime import datetime, timedelta, timezone


app = Flask(__name__)

api = Api(app, doc='/swagger')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy()

load_dotenv()
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')


app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config['JWT_COOKIE_CSRF_PROTECT'] = False # Only False while testing
app.config["JWT_COOKIE_SECURE"] = False # Only false while in testing
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
jwt = JWTManager(app)


cors = CORS(app, resources={r"/*": {"origins": ["https://ccse-gjcrbsexd6bhaheb.canadacentral-01.azurewebsites.net", "http://client:80"]}})

db.init_app(app)

'''@app.before_request
def protect_swagger_docs():
    # Assuming your docs are served at '/swagger' and '/swagger.json'
    if request.path.startswith('/swagger'):
        # This will raise an error if JWT is missing or invalid.
        try:
            verify_jwt_in_request(optional=False)
            jwt_data = get_jwt()
                
            # Check if "role" exists in the JWT claims and includes "admin"
            role = jwt_data.get("role", [])
            if "admin" not in role:
                return jsonify({"msg": "Admins only"})

        except Exception as e:
            return jsonify({"msg": "Missing or invalid JWT"})'''

@app.after_request
@jwt_required
def refresh_expiring_jwts(response):
    try:
        print("aaaaaaa")
        exp_timestamp = get_jwt()["exp"] # Find out when it expired
        now = datetime.now(timezone.utc) # Get current time
        target_timestamp = datetime.timestamp(now + timedelta(minutes=10)) # Gets time 10 mins ahead
        if target_timestamp > exp_timestamp: # If token is going to expire within 10 mins
            access_token = create_access_token(identity=get_jwt_identity()) # Make a new access token for the same identity
            set_access_cookies(response, access_token) # Set the access cookie to new token
        return jsonify(response)
    except (RuntimeError, KeyError):
        print("bbbbbbbb")
        print(request.cookies)
        # Case where there is not a valid JWT. Return 'Invalid JWT' message
        return jsonify({"msg" : "Invalid JWT"})



@dataclass #Used for verifying data and documentation
class User(db.Model): #Model for the DB

    id: int #sets the expected data types for when JSONified
    username: str
    password: str
    role : str

    __tablename__ = 'Users' #Set tablename
    id: Mapped[int] = mapped_column(unique=True, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)

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

    __tablename__ = 'Orders'
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    orderFulfilled: Mapped[bool] = mapped_column(nullable=False)
    customerID: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)


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
    #db.drop_all() #TODO remove
    db.create_all()

#testUser = User(username='test', email='')

'''@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return jsonify(request.cookies)
        #return {'hello': User.query.all()}'''
        



'''@api.route('/postshit', methods=['POST']) # TODO REMOVE
class postShit(Resource):
    @api.doc(parser=parser)
    def post(username):
        args = parser.parse_args()
        #db.session.add(testUser)
        #db.session.commit()

        return 'Hello, ' + args['username']'''
        
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    try:
        print("getting user")
        identity = jwt_data["sub"]
        print("got identity")
        return jsonify({User.query.filter_by(id=identity).first()})
    except:
        print("error")
        return jsonify({"msg":"Failed lookup"})


#LOGIN:

#GetLoginInfo
#   Get the Post request
#   Check if there is a JWT -> different method
#   Check if creds correct (Later implement a DB system for this)
#   return a login token

LoginModel = api.model('LoginModel', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

@api.route('/login', methods=['POST'])
class login(Resource):
    @api.expect(LoginModel, validate=True) #Ensure username and password is the only data in POST request
    @jwt_required(optional=True)
    def post(self):
        data = request.get_json() # Get inputted data
        current_identity = get_jwt_identity()
        if current_identity:
            return jsonify({"msg":"Already Logged In"})
        else:
            try:
                user = User.query.filter_by(username=data['username']).first() # Check if the username matches a user
                if user and check_password_hash(user.password, data["password"]): # Compare inputted password against the hash
                    user = User.query.filter_by(username=data['username']).first()
                    role = {"role" : str(user.role), "id" : user.id}
                    access_token = create_access_token(identity=str(user.id), additional_claims=role) # Set the access token
                    refresh_token = create_refresh_token(identity=str(user.id), additional_claims=role) # Set the refresh token
                    response = jsonify({"msg": "Login Success"})
                    set_access_cookies(response, access_token) # Sets the cookies
                    set_refresh_cookies(response, refresh_token)
                    return response
                else:
                    return jsonify({"msg": "Incorrect Credentials"})
            except:
                return jsonify({"msg":"Error"})

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
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

@api.route('/register', methods=['POST'])
class register(Resource):
    @api.expect(RegisterModel, validate=True) #Ensure username and password is the only data in POST request
    def post(self):
        data = request.get_json()
        try:
            checkUser = User.query.filter_by(username=data['username']).first() # Check for users with the same username
            if checkUser:
                return jsonify({"msg": "User already exists"})
            #Create newUser object with the username and hash of the password, role is always user
            newUser = User(username=data['username'],password=generate_password_hash(data['password'], 'scrypt'), role="user")
            db.session.add(newUser) # Adds user to table
            db.session.commit() # Makes the changes permanent
            return jsonify({"msg": "Success"})
        except:
            return jsonify({"msg": "Error"})

#ADMIN:
#TODO Make user into seller

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


@api.route('/userdetails/<int:id>', methods=['GET'])
class getUserDetails(Resource):
    @jwt_required()
    def get(self, id):
        role = get_jwt()
        if role["role"] == "admin":
            userDetails = User.query.filter_by(id=id).all()
            return jsonify(userDetails)
        else:
            return jsonify({"msg":"Unauthorized"})

@api.route('/getallusers', methods=['GET'])
class getAllUsers(Resource):
    @jwt_required()
    def get(self):
        role = get_jwt()
        if role["role"] == "admin": # check if user is admin
            userDetails = User.query.all() # get all users
            return jsonify(userDetails)
        else:
            return jsonify({"msg": "Unauthorized"})
        
@api.route('/makeseller/<int:id>', methods=['GET'])
class getAllUsers(Resource):
    @jwt_required()
    def get(self, id):
        role = get_jwt()
        if role["role"] == "admin": # check if user is admin
            userDetails = User.query.filter_by(id=id).first() # get single user
            userDetails.role = "seller"
            return jsonify({"msg": "user is now seller"})
        else:
            return jsonify({"msg": "Unauthorized"})


#Check Orders:
#   Get all orders with customerID as the users

@api.route('/getallorders/<int:customerID>', methods=['GET'])
class getOrders(Resource):
    def getAll(self, customerID):
        pass

#Check Basket:
#   TODO

#SELLER PAGE:

#Show current products
#   Get all products with sellerID as the sellers one
@api.route('/getsellerproducts/<int:id>', methods=['GET']) #id is the seller ID
class getsellerproducts(Resource):
    @jwt_required()
    def get(self, id):
        role = get_jwt()
        if role["role"] == "seller" and current_user.identity == id:
            products = Products.query.filter_by(owner=id).all()
            return jsonify(products)
        else:
           return jsonify({"msg" : "Unathorised"})

#Sellers Report
#   TODO

#Add new product
#   Parse the form data
#   Add new item to the database

ProductModel = api.model('ProductModels', {
    'name': fields.String(required=True),
    'description': fields.String(required=True),
    'seller': fields.Integer(required=True),
    'cost' : fields.Integer(required=True)
    })

@api.route('/addproduct', methods=['POST'])
class addProduct(Resource):
    @api.expect(ProductModel, validate=True) #When validating check errors aren't returned to users TODO
    @jwt_required
    def post(self):
        try:
            role = get_jwt()
            if role["role"] == "seller": # Check 
                try:
                    data = request.get_json()
                    newProduct = Products(name=data['name'],description=data['description'],owner=data['seller'],cost=data['cost'],numberSold=0)
                    db.session.add(newProduct)
                    db.session.commit()
                    result = Products.query.filter_by(name=data['name']).all()
                    return jsonify({"msg" : "Success", "object" : result})
                except:
                    return jsonify({"msg": "Product not added"})
            else:
                return jsonify({"msg" : "Unauthorised"})
        except:
            return jsonify({"msg": "Product not added"})

#Edit current product
#   POST
#   Recieves product in JSON
#   Updates every value of the product in the database

@api.route('/editproduct/<int:id>', methods=['POST'])
class editProduct(Resource):
    @api.expect(ProductModel, validate=True)
    def post(self, id):
        data = request.get_json()
        product = Products.query.filter_by(id=id).first()
        product.name = data['name']
        product.description = data['description']
        product.owner = data['seller']
        product.cost = data['cost']
        db.session.commit()

@api.route('/deleteproduct/<int:id>', methods=['GET'])
class deleteProduct(Resource):
    def get(self, id):
        Products.query.filter_by(id=id).delete()
        db.session.commit()

@api.route('/getsingleproduct/<int:id>', methods=['GET'])
class getSingleProduct(Resource):
    def get(self, id):
        product = Products.query.filter_by(id=id).first()
        return jsonify({"msg": "Success", "product": product})

@api.route('/getproducts', methods=['GET'])
class getProducts(Resource):
    def get(self):
        products = Products.query.all()
        return jsonify({"msg": "Success", "products": products})

@api.route('/userinfo', methods=['GET'])
class userInfo(Resource):
    @jwt_required()
    def get(self):
        try:
            user = get_jwt()
            return jsonify({"role": user["role"], "id" : user["id"]})
        except:
            return jsonify({"msg":"Failed"})


#IMAGES


'''#TODO change the model to actually be like an image
ImageModel = api.model('ImageModel', {
    'filelocation': fields.String(required=True),
    })

@api.route('/uploadimage', methods=['POST'])
class uploadImage(Resource):
    #@api.expect(ImageModel, validate=True)
    def post(self):
        data = request.get_json()
        print(data)
        image = data['file']
        print(image)
        #with open("./funnyimage", 'wb') as file:
         #   file.write(image)
        return jsonify({'msg': 'Success'})'''


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

