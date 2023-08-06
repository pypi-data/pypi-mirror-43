from flask import Flask, request
from flask_restful import reqparse, Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug = True)
