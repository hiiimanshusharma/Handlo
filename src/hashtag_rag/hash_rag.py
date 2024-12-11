import os
import torch
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
from llama_index.core import Settings, SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI

load_dotenv(dotenv_path = './config/.env')

HF_TOKEN = os.getenv("HF_TOKEN")

Settings.embed_model = FastEmbedEmbedding()
Settings.llm = HuggingFaceInferenceAPI(
    model_name="mistralai/Mistral-7B-Instruct-v0.3", token=HF_TOKEN, temperature=0.1
)

dir =  Path(f"~/handlo/data/hash_dir").expanduser()

documents = SimpleDirectoryReader(input_files=dir.iterdir()).load_data()

client = QdrantClient(path="~/handlo/vectorDB/")

vector_store = QdrantVectorStore(client=client, collection_name="collection-v1",  prefer_grpc=True)
storage_context = StorageContext.from_defaults(
                    vector_stores={'default': vector_store}
                )

# storage_context.persist(persist_dir="~/handlo/data/storage_context")

index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
)

index.storage_context.persist(persist_dir="~/handlo/data/storage_context")