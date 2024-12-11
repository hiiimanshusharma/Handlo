from pathlib import Path

images = Path('/home/himanshu/handlo/data/him2.jpg')

img_var = images.read_bytes()

img_str = img_var.decode('latin1')

print(img_str)