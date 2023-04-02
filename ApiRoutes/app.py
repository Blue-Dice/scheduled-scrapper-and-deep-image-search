from flask import Flask, request
from Helpers import Logger as Log
from typing import Any
from decouple import config
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

class ProductService():
    
    def __init__(self) -> None:
        self.port = config("FLASK_PORT", default=3000, cast=int)
        self.host = config("FLASK_HOST", default="0.0.0.0", cast=str)
        self.debug = config("FLASK_DEBUG", default=True, cast=bool)
        self.flask_secret_key = config("FLASK_SECRET_KEY", default=None, cast=str)
        self.enable_csrf_protection = config("ENABLE_FLASK_CSRF", default=False, cast=bool)
    
    def response(self, status: int = 200, message: str = None, data: str|Any = None) -> tuple[dict,int]:
        context = {}
        context["Data"] = data
        context["Error"] = False if (200 <= status <= 299) else True
        context["Status"] = status
        context["Message"] = message
        result = f"{status} -> {context}"
        Log.error(result) if context["Error"] else Log.success(result)
        return context, status
    
    def run(self) -> None:
        app = Flask(__name__)
        app.secret_key = self.flask_secret_key
        app.config["WTF_CSRF_ENABLED"] = self.enable_csrf_protection
        CORS(app)
        CSRFProtect(app)
        app.route("/", methods=["GET", "POST"])(self.index)
        app.route("/get-similar-products", methods=["GET", "POST"])(self.similar_product_lookup)
        app.run(self.host, self.port, self.debug)
    
    def index(self) -> tuple[dict,int]:
        return self.response(200, f"Message successfully recieved from {request.remote_addr}")
    
    def get_product_status(self):
        pass
    
    def similar_product_lookup(self):
        pass
    
    def get_product_information(self):
        pass