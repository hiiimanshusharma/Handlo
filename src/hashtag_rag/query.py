import os
from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import Settings, SimpleDirectoryReader, StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from llama_index.core import PromptTemplate

load_dotenv(dotenv_path = './src/configurations/.env')

HF_TOKEN = os.getenv("HF_TOKEN")

Settings.embed_model = FastEmbedEmbedding()
Settings.llm = HuggingFaceInferenceAPI(
    model_name=os.getenv("MODEL_NAME"), token=HF_TOKEN, temperature=0.1
)


class HashtagRetriever():
    def __init__(self):
        self.query = """
                    You are a helpful AI assistant that suggests hashtags from the sentence: {sentence}. 
                    On the basis of mood, object, and place from the provided sentence and use them to generate relevant hashtags. 
                    If the sentence doesn't contain enough information, just say 'Not enough information'.
                """
        self.BASE_PATH = os.getenv("BASE_PATH")
        
    def get_query_engine(self):
        persist_dir = Path(f"{self.BASE_PATH}/data/storage_context").expanduser()
        client = QdrantClient(path=f"{self.BASE_PATH}/vectorDB/hashtags.db")
        vector_store = QdrantVectorStore(client=client, collection_name="collection-v1", prefer_grpc=True)
        storage_context = StorageContext.from_defaults(
                            vector_stores={'default': vector_store},
                            persist_dir=persist_dir
                        )
        index = load_index_from_storage(storage_context)
        query_engine = index.as_query_engine()
        return query_engine

    def get_hashtags(self, sentence):
        response = self.get_query_engine().query(self.query.format(sentence=sentence))
        return response
    

# if __name__ == "__main__":
#     hr = HashtagRetriever()
#     sentence = "Sitting down with my furry friend, I'm grateful for the moments of calm in my life."
#     response = hr.get_hashtags(sentence)
#     print(response)


