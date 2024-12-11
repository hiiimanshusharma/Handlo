import torch
import requests
from PIL import Image
from io import BytesIO
from transformers import BlipProcessor, BlipForConditionalGeneration

class ContextRetriever():
    def __init__(self):
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device) 
        
    def get_context(self, img_str):
        img_bytes = img_str.encode('latin1')
        raw_image = Image.open(BytesIO(img_bytes)).convert('RGB')
        text = ""
        inputs = self.processor(raw_image, text, return_tensors="pt").to(self.device)
        out = self.model.generate(**inputs)
        return self.processor.decode(out[0], skip_special_tokens=True)



