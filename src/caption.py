from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

torch.manual_seed(0)

class Caption:

    def __init__(self, context: str = None, mood: str = None):
        self.model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model)
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        self.context = context
        self.mood = mood



    def generate_prompt(self):
        prompt = f"Generate caption for the image context provided below with {self.mood}:\nContext: {self.context}\nCaption:\n"
        return prompt

    def generate_captions(self, max_new_tokens: int = 50):
        prompt = self.generate_prompt()
        sequences = self.pipe(
            prompt,
            max_new_tokens=max_new_tokens,
        )

        captions = []
        for seq in sequences:
            caption = seq['generated_text'].split("Caption:")[1].strip()
            captions.append(caption)

        return captions

# context = "a photography of a woman in a white swimsuit at a beach bar"
# mood = "humor"
# cap_obj = Caption(context=context, mood=mood)

# captions = cap_obj.generate_captions()
# print(captions)