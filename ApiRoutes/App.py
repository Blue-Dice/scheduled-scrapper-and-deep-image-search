from flask import Flask, request
from typing import Any
from Helpers import Logger as Log
from decouple import config
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from ImageSimilarity.IndexSearch import SimilarityIndex

class ProductService():
    
    def __init__(self) -> None:
        self.SI = SimilarityIndex()
        self.wash_meta()
        self.port = config("FLASK_PORT", default=3000, cast=int)
        self.host = config("FLASK_HOST", default="0.0.0.0", cast=str)
        self.debug = config("FLASK_DEBUG", default=True, cast=bool)
        self.flask_secret_key = config("FLASK_SECRET_KEY", default=None, cast=str)
        self.enable_csrf_protection = config("ENABLE_FLASK_CSRF", default=False, cast=bool)
    
    def wash_meta(self) -> None:
        img = [
            "https://img.freepik.com/free-vector/white-plates-realistic-3d-ceramic-dishes-top-side-view-collection_107791-3743.jpg?size=626&ext=jpg",
            "https://img.freepik.com/free-vector/realistic-white-plate-isolated_1284-41743.jpg?size=626&ext=jpg",
            "https://img.freepik.com/free-photo/plate-mat-with-plate-fork-knife_1339-2898.jpg?size=626&ext=jpg",
            "https://img.freepik.com/free-photo/cutlery-overhead-wooden-dining-food_1203-6082.jpg?size=626&ext=jpg",
            "https://img.freepik.com/free-psd/close-up-ceramic-plate-mockup_53876-98747.jpg?size=626&ext=jpg",
            "https://img.freepik.com/free-vector/top-view-white-different-shapes-bowls_1441-4212.jpg?size=626&ext=jpg"
        ]
        self.SI.rebase_vectors_and_features(img)
        self.SI.load_metadata()
    
    def response(self, status: int = 200, message: str = None, data: str|Any = None) -> tuple[dict,int]:
        context = {}
        context["Data"] = data
        context["Error"] = False if (200 <= status <= 299) else True
        context["Status"] = status
        context["Message"] = message
        result = f"{status} -> {context.get('Message')}"
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
    
    def get_product_status(self) -> tuple[dict,int]: # bypass linter
        pass # bypass linter
    
    def similar_product_lookup(self) -> tuple[dict,int]:
        img = "https://img.freepik.com/free-psd/close-up-ceramic-plate-mockup_53876-98747.jpg?size=626&ext=jpg"
        return self.response(
            200,
            "Similarity search successful",
            self.SI.fetch_similar_images(img)
        )
    
    def get_product_information(self) -> tuple[dict,int]: # bypass linter
        pass # bypass linter