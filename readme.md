# Handlo
RAG for Hashtag generation for image context retrieved through VLM
---

### Setup
./src/requirements
```
$ pip install -r base.txt
```

#### Starting backend server
./src
```
$ python app.py
```

#### Frontend
```
$ streamlit run stream_app.py
```

### Demo


### Technology used overview
* For context retrieval from image used [salesforce BLIP model](https://huggingface.co/Salesforce/blip-image-captioning-base)
* For caption generation used [TinyLlama Model](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0)
* Created RAG for hastrag prediction using [LlamaIndex](https://docs.llamaindex.ai/en/stable/)
* For RAG used [Twitter Hashtag Dataset](https://huggingface.co/datasets/Twitter/HashtagPrediction/blob/main/hashtag-classification-id.zip)
* Backend API created using FastAPI
* User Interface created using Streamlit Framework.


---
for more info refer conceptual documentation:  