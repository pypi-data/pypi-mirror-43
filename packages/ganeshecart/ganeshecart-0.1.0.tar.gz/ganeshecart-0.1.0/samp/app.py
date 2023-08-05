from app import *
from flask import Flask, request
from flask_restful import reqparse, Api
from flask_cors import CORS
app = Flask(__name__)
api = Api(app)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug = True)
