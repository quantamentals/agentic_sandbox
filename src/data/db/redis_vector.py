import json
import redis
from redis.commands.search.field import VectorField, TagField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
# from sentence_transformers import SentenceTransformer

from src.data.db.vector_base import VectorDatabase

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Initialize SentenceTransformer model
model = None  # some embedding model from the current ensemble

class RedisVectorDB(VectorDatabase):
    """
    The RedisVectorDB class provides methods to:

    create_index: Create a Redis index for storing vectorized items.
    load_items: Load JSON items and store them in Redis as vectors.
    retrieve_similar_items: Retrieve similar items based on vector similarity.
    """
    def __init__(self, redis_client, index_name, model_name):
        super().__init__(redis_client, index_name, model_name)

    def create_index(self):
        try:
            self.redis_client.ft(self.index_name).info()
        except redis.exceptions.ResponseError:
            schema = (
                VectorField("vector", "FLAT", {"TYPE": "FLOAT32", "DIM": 384, "DISTANCE_METRIC": "COSINE"}),
                TextField("title"),
                TextField("text"),
                TagField("article_type"),
                TagField("application")
            )
            definition = IndexDefinition(prefix=[f"{self.index_name}:"])
            self.redis_client.ft(self.index_name).create_index(schema, definition=definition)

    def load_items(self, json_file):
        with open(json_file, 'r') as f:
            items = json.load(f)
        for item in items:
            vector = self._encode_text(item['text'])
            self.redis_client.hset(f"{self.index_name}:{item['item_id']}", mapping={
                "vector": vector.tobytes(),
                "title": item['title'],
                "text": item['text'],
                "article_type": item['article_type'],
                "application": item['application']
            })

    def retrieve_similar_items(self, query_text, top_k=5):
        query_vector = self._encode_text(query_text)
        query_params = {"query_vector": query_vector.tobytes()}
        query = f"(*)=>[KNN {top_k} @vector $query_vector AS vector_score]"
        results = self.redis_client.ft(self.index_name).search(query, query_params=query_params).docs
        similar_items = []
        for result in results:
            similar_items.append({
                "item_id": result.id.split(":")[1],
                "title": result.title,
                "text": result.text,
                "article_type": result.article_type,
                "application": result.application,
                "score": result.vector_score
            })
        return similar_items