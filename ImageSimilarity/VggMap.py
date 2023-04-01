from io import BytesIO
from Helpers import Logger as Log
from keras.utils import load_img, img_to_array
from sklearn.metrics.pairwise import cosine_similarity
from keras.applications.vgg16 import VGG16, preprocess_input
import h5py
import numpy as np
import requests

class FeatureMapping():
    
    def __init__(self) -> None:
        self.model = VGG16(weights="imagenet", include_top=False)
        self.similarity_threshold = 0.5
        self.features_file = "FeatureIndices.h5"
    
    def save_features(self) -> None:
        try:
            with h5py.File(self.features_file, "w") as file:
                file.create_dataset("features", data=np.array(self.target_feats))
                file.create_dataset("urls", data=np.array(self.target_urls))
            Log.success("Image feature indices saved successfully")
        except Exception as e:
            Log.error(f"Error while saving image feature indices -> {e}")
    
    def load_features(self) -> None:
        try:
            with h5py.File(self.features_file, "r") as file:
                self.target_feats = file["features"][:]
                self.target_urls = file["urls"][:]
            Log.success("Image feature indices loaded successfully")
        except Exception as e:
            Log.error(f"Error while loading saved image features -> {e}")
        
    def extract_features(self, image_urls: list):
        try:
            self.target_feats = []
            self.target_urls = []
            for image_url in image_urls:
                response = requests.get(image_url)
                target_img = load_img(BytesIO(response.content), target_size=(224, 224))
                target_img = img_to_array(target_img)
                target_img = np.expand_dims(target_img, axis=0)
                target_img = preprocess_input(target_img)
                target_feat = self.model.predict(target_img).ravel()
                self.target_feats.append(target_feat)
                self.target_urls.append(image_url)
            Log.success("Image feature indices extracted successfully")
        except Exception as e:
            Log.error(f"Error while extracting saved image features -> {e}")
    
    def fetch_similar_images(self, query_url) -> None:
        try:
            response = requests.get(query_url)
            query_img = load_img(BytesIO(response.content), target_size=(224, 224))
            query_img = img_to_array(query_img)
            query_img = np.expand_dims(query_img, axis=0)
            query_img = preprocess_input(query_img)
            query_feat = self.model.predict(query_img).ravel()
            similarity_scores = cosine_similarity([query_feat], self.target_feats)[0]
            similar_images = [
                self.target_urls[i] for i in range(len(similarity_scores)) if similarity_scores[i] > self.similarity_threshold
            ]
            Log.success(f"Similarity search successful!")
            return similar_images
        except Exception as e:
            Log.error(f"Error while running similarity search -> {e}")