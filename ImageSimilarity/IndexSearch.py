from Helpers import Logger as Log
from ImageSimilarity.VggFeaturing import FeatureMap
import requests

class SimilarityIndex():
    
    def __init__(self) -> None:
        self.VggController = FeatureMap()
        self.VggController.load_model()
    
    def rebase_vectors_and_features(self, image_urls: list) -> None:
        image_data, target_vecs = self.VggController.fetch_image_features(image_urls)
        self.VggController.save_metadata(image_data, target_vecs)
    
    def load_metadata(self) -> None:
        self.image_data, self.target_vecs = self.VggController.load_metadata()
        
    def fetch_similar_images(self, query_url: str, query_num: int = 5) -> list:
        try:
            response = requests.get(query_url)
            query_feat = self.VggController.extract_features(response.content)
            index_list = self.target_vecs.get_nns_by_vector(query_feat, query_num)
            return self.image_data.iloc[index_list]['target_urls'].to_list()
        except Exception as e:
            Log.error(f"Error while running similarity search -> {e}")