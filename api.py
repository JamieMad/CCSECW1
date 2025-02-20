from flask import Flask, request, jsonify
from flask_restx import Resource, Api, reqparse, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from dataclasses import dataclass
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, current_user, set_access_cookies, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timedelta, timezone


app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy()

app.config['JWT_SECRET_KEY'] = 'super-secret-key-please-make-it-longer-aaahhh'
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
jwt = JWTManager(app)


db.init_app(app)

cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000/*"}})

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=10))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response



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

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return jsonify(request.cookies)
        #return {'hello': User.query.all()}
        


parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help='username')
parser.add_argument('password', type=str, required=True, help='password')



@api.route('/postshit', methods=['POST'])
class postShit(Resource):
    @api.doc(parser=parser)
    def post(username):
        args = parser.parse_args()
        #db.session.add(testUser)
        #db.session.commit()

        return 'Hello, ' + args['username']
        
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()

#LOGIN:

#GetLoginInfo
#   Get the Post request
#   Check if there is a JWT -> different method
#   Check if creds correct (Later implement a DB system for this)
#   return a login token

LoginModel = api.model('LoginModel', {
    'username': fields.String,
    'password': fields.String(required=True)
})

@api.route('/login', methods=['POST'])
class login(Resource):
    @api.expect(LoginModel, validate=True) #When validating check errors aren't returned to users TODO
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password, data["password"]):
            access_token = create_access_token(identity=str(user.id))
            response = jsonify({"msg": "Login Success"})
            set_access_cookies(response, access_token)
            return response
        else:
            return jsonify({"msg": "login failed"})

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

        checkUser = User.query.filter_by(username=data['username']).first()
        if checkUser:
            return jsonify({"msg": "User already exists"})

        newUser = User(username=data['username'],password=generate_password_hash(data['password'], 'scrypt'), role="admin")
        db.session.add(newUser)
        db.session.commit()
        result = User.query.filter_by(username=data['username'])
        return jsonify({"msg": "Success"})

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

parser = api.parser()
parser.add_argument('X-CSRF-TOKEN', location='headers')

@api.route('/userdetails/<int:id>', methods=['GET']) #TODO Admin only
class getUserDetails(Resource):
    @api.expect(parser)
    @jwt_required()
    def get(self, id):
        if current_user.role == "admin":
            userDetails = User.query.filter_by(id=id).all()
            return jsonify(userDetails)
        else:
            return jsonify({"msg":"Unauthorized"})

@api.route('/getallusers', methods=['GET']) #TODO remove this
class getAllUsers(Resource):
    @api.expect(parser)
    @jwt_required()
    def get(self):
        if current_user.role == "admin":
            userDetails = User.query.all()
            return jsonify(userDetails)
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
    def get(self, id):
        products = Products.query.filter_by(owner=id).all()
        return jsonify(products)

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
    def post(self):
        data = request.get_json()
        newProduct = Products(name=data['name'],description=data['description'],owner=data['seller'],cost=data['cost'],numberSold=0)
        db.session.add(newProduct)
        db.session.commit()
        result = Products.query.filter_by(name=data['name']).all()
        return jsonify(result)

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
    


#IMAGES


#TODO change the model to actually be like an image
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
        return jsonify({'msg': 'Success'})


if __name__ == '__main__':
    app.run(debug=True)