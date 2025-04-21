import sqlite3
import numpy as np

from src.data.db.vector_base import VectorDatabase

class SQLiteVectorDB(VectorDatabase):
    """
    The SQLiteVectorDB class provides methods to:

    create_table: Create a SQLite table for storing vectorized items.
    load_items: Load JSON items and store them in SQLite as vectors.
    retrieve_similar_items: Retrieve similar items based on vector similarity.
    """
    def __init__(self, db_name, table_name, model_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.table_name = table_name
        self.create_table()
        super().__init__(None, table_name, model_name)

    def create_table(self):
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                item_id INTEGER PRIMARY KEY,
                vector BLOB,
                title TEXT,
                text TEXT,
                article_type TEXT,
                application TEXT
            )
        """)
        self.conn.commit()

    def load_items(self, json_file):
        with open(json_file, 'r') as f:
            items = json.load(f)
        for item in items:
            vector = self._encode_text(item['text'])
            self.cursor.execute(f"""
                INSERT INTO {self.table_name} (item_id, vector, title, text, article_type, application)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                item['item_id'],
                vector.tobytes(),
                item['title'],
                item['text'],
                item['article_type'],
                item['application']
            ))
        self.conn.commit()

    def retrieve_similar_items(self, query_text, top_k=5):
        query_vector = self._encode_text(query_text)
        self.cursor.execute(f"""
            SELECT item_id, title, text, article_type, application, vector
            FROM {self.table_name}
        """)
        results = self.cursor.fetchall()
        similar_items = []
        for result in results:
            item_id, title, text, article_type, application, vector = result
            vector = np.frombuffer(vector)
            score = np.dot(query_vector, vector) / (np.linalg.norm(query_vector) * np.linalg.norm(vector))
            similar_items.append({
                "item_id": item_id,
                "title": title,
                "text": text,
                "article_type": article_type,
                "application": application,
                "score": score
            })
        similar_items.sort(key=lambda x: x['score'], reverse=True)
        return similar_items[:top_k]
    

if __name__ == "__main__":
    vector_db = SQLiteVectorDB("vector_db.db", "items", "all-MiniLM-L6-v2")
    vector_db.load_items("items.json")
    similar_items = vector_db.retrieve_similar_items("How to create a new user?")
    print(similar_items)    