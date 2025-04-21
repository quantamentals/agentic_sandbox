from abc import ABC, abstractmethod
# from sentence_transformers import SentenceTransformer
import redis


#TODO: run utils function to seed the redis with vector base intents

#TODO:  take json of vectorized intent and resources and load into vectordb

#TODO: use a similarity search algo to retrive intents and resources
class VectorDatabase(ABC):
    def __init__(self, db_client, index_name: str, model_name: str=None):
        self.db_client = db_client
        self.index_name = index_name
        self.model = None
        self.create_index()

    @abstractmethod
    def create_index(self):
        pass

    @abstractmethod
    def load_data(self, data):
        pass

    @abstractmethod
    def retrieve_similar(self, query_text: str, top_k: int):
        pass

    def _encode_text(self, text: str):
        return self.model.encode(text)

    def _get_vector(self, text: str):
        return self._encode_text(text).tobytes()