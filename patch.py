from ImageSimilarity.IndexSearch import SimilarityIndex

img1 = [
    "https://img.freepik.com/free-vector/white-plates-realistic-3d-ceramic-dishes-top-side-view-collection_107791-3743.jpg?size=626&ext=jpg",
    "https://img.freepik.com/free-vector/realistic-white-plate-isolated_1284-41743.jpg?size=626&ext=jpg",
    "https://img.freepik.com/free-photo/plate-mat-with-plate-fork-knife_1339-2898.jpg?size=626&ext=jpg",
    "https://img.freepik.com/free-photo/cutlery-overhead-wooden-dining-food_1203-6082.jpg?size=626&ext=jpg",
    "https://img.freepik.com/free-vector/top-view-white-different-shapes-bowls_1441-4212.jpg?size=626&ext=jpg"
]

img2 = "https://img.freepik.com/free-psd/close-up-ceramic-plate-mockup_53876-98747.jpg?size=626&ext=jpg"

if __name__ == "__main__":
    controller = SimilarityIndex()
    controller.rebase_vectors_and_features(img1)
    controller.load_metadata()
    result = controller.fetch_similar_images(img2)
    print(result)