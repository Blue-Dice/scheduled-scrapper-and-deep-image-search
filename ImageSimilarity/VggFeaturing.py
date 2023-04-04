from io import BytesIO
from tqdm import tqdm
from annoy import AnnoyIndex
from Helpers import Logger as Log
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras.utils import load_img, img_to_array
from keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.python.keras.models import Model
import numpy as np
import pandas as pd
import requests

class FeatureMap():
    
    def __init__(self) -> None:
        self.meta_data_file = f"{os.getcwd()}/Image-metadata"
        self.vector_file = f"{self.meta_data_file}/ImageVectorIndices.ann"
        self.feature_file = f"{self.meta_data_file}/ImageFeatureIndices.pkl"
    
    def load_model(self) -> None:
        try:
            base_model = VGG16(weights="imagenet")
            self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
            Log.success("VGG16 [weights: imagenet] [output-layer: fc1] model loaded successfully")
        except Exception as e:
            Log.error(f"Error while loading VGG16 model -> {e}")
            
    def save_features(self, image_data: pd.DataFrame) -> None:
        try:
            image_data.to_pickle(self.feature_file)
            Log.success("Image features saved successfully: [Image-metadata/ImageFeatureIndices.pkl]")
        except Exception as e:
            Log.error(f"Error while saving image feature indices -> {e}")
    
    def save_vectors(self, target_vecs: AnnoyIndex) -> None:
        try:
            target_vecs.save(self.vector_file)
            Log.success("Image vectors saved successfully: [Image-metadata/ImageVectorIndices.ann]")
        except Exception as e:
            Log.error(f"Error while saving image vector indices -> {e}")
    
    def save_metadata(self, image_data: pd.DataFrame, target_vecs: AnnoyIndex) -> None:
        if not os.path.isdir(self.meta_data_file):
            os.mkdir(self.meta_data_file)
        self.save_features(image_data)
        self.save_vectors(target_vecs)
            
    def load_metadata(self) -> tuple[pd.DataFrame, AnnoyIndex]:
        try:
            image_data = pd.read_pickle(self.feature_file)
            feature_length = len(image_data['target_feats'][0])
            target_vecs = AnnoyIndex(feature_length, 'euclidean')
            target_vecs.load(self.vector_file)
            Log.success("Image metadata loaded successfully")
            return image_data, target_vecs
        except Exception as e:
            Log.error(f"Error while loading image metadata -> {e}")
    
    def extract_vectors(self, image_data: pd.DataFrame) -> AnnoyIndex:
        try:
            feature_length = len(image_data['target_feats'][0])
            target_vecs = AnnoyIndex(feature_length, 'euclidean')
            for index, vector in tqdm(zip(image_data.index, image_data['target_feats']), disable=True):
                target_vecs.add_item(index, vector)
            target_vecs.build(100)
            Log.success("Image vector indices extracted successfully")
            return target_vecs
        except Exception as e:
            Log.error(f"Error while extracting saved image vectors -> {e}")
    
    def extract_features(self, image: bytes) -> np.ndarray|None:
        try:
            image = load_img(BytesIO(image), target_size=(224, 224))
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)
            image = preprocess_input(image)
            target_feat = self.model.predict(image)[0]
            return target_feat / np.linalg.norm(target_feat)
        except Exception as e:
            Log.error(f"Error extracting image features -> {e}")
            return None
        
    def fetch_features_and_vectors(self, image_urls: list) -> tuple[pd.DataFrame, AnnoyIndex]:
        try:
            image_data = pd.DataFrame()
            target_urls = []
            target_feats = []
            for image_url in image_urls:
                response = requests.get(image_url)
                target_feats.append(self.extract_features(response.content))
                target_urls.append(image_url)
            image_data['target_urls'] = target_urls
            image_data['target_feats']  = target_feats
            image_data = image_data.dropna().reset_index(drop=True)
            Log.success("Image feature indices extracted successfully")
            return image_data, self.extract_vectors(image_data)
        except Exception as e:
            Log.error(f"Error while extracting saved image features -> {e}")