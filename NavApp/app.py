from flask import Flask, request
from Helpers import Logger as Log
from decouple import config
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = config('FLASK_SECRET_KEY', cast=str)
app.config['WTF_CSRF_ENABLED'] = config('CSRF_ENABLED', cast=bool)
CORS(app)
CSRFProtect(app)

class ProductService():
    
    def __init__(self) -> None:
        pass
    
    def initiliaze_app(self):
        pass
    
    def get_product_status(self):
        pass
    
    def similar_product_lookup(self):
        pass
    
    def get_product_information(self):
        pass

if __name__ == '__man__':
    ProductService().initiliaze_app()