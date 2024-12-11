import requests
from pathlib import Path

api_url = 'http://127.0.0.1:8000/{endpoint}'
context_endpoint = 'get-context'
caption_endpoint = 'get-caption'
hashtags_endpoint = 'get-hashtags'

image_path = input('Enter the path of the image: ')
images = Path(image_path)

print(type(images))

img_var = images.read_bytes()
print(type(img_var))
img_str = img_var.decode('latin1')

response = requests.post(api_url.format(endpoint=context_endpoint), json={'img_bytes': img_str})
# print(response.json())
context = response.json()['context']
print({'context': context, 'status':response.status_code})

# mood = input('Enter the mood: ')
mood = "calm"

cap_url = 'http://127.0.0.1:8000/get-caption'
response = requests.post(api_url.format(endpoint=caption_endpoint), json={'context': context, 'mood':mood})
print({'caption': response.json()['captions'], 'status':response.status_code})

response = requests.post(api_url.format(endpoint=hashtags_endpoint), json={'sentence': 'Sitting down with my furry friend, I\'m grateful for the moments of calm in my life.'})
print({'hashtags': response.json()['hashtags']['response'], 'status':response.status_code})
