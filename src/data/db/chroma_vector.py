import chromadb

from src.data.db.vector_base import VectorDatabase

class ChromaVectorDB(VectorDatabase):
    """
    The ChromaVectorDB class provides methods to:

    create_collection: Create a ChromaDB collection for storing vectorized items.
    load_items: Load JSON items and store them in ChromaDB as vectors.
    retrieve_similar_items: Retrieve similar items based on vector similarity.
    """
    def __init__(self, host, port, collection_name, model_name):
        self.client = chromadb.HttpClient(host=host, port=port)
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(collection_name)
        super().__init__(None, collection_name, model_name)

    def create_index(self):
        # ChromaDB doesn't require explicit index creation
        pass

    def load_items(self, json_file):
        with open(json_file, 'r') as f:
            items = json.load(f)
        for item in items:
            vector = self._encode_text(item['text'])
            self.collection.add(
                ids=[str(item['item_id'])],
                embeddings=[vector.tolist()],
                metadatas=[{
                    "title": item['title'],
                    "text": item['text'],
                    "article_type": item['article_type'],
                    "application": item['application']
                }]
            )

    def retrieve_similar_items(self, query_text, top_k=5):
        query_vector = self._encode_text(query_text)
        results = self.collection.query(
            query_embeddings=[query_vector.tolist()],
            n_results=top_k
        )
        similar_items = []
        for i, result in enumerate(results['ids'][0]):
            metadata = results['metadatas'][0][i]
            similar_items.append({
                "item_id": result,
                "title": metadata['title'],
                "text": metadata['text'],
                "article_type": metadata['article_type'],
                "application": metadata['application'],
                "score": results['distances'][0][i]
            })
        return similar_items