import os
from PIL import Image

formats = ['.png', '.jpg', '.jpeg'] # in case of extension 'JPEG'
size = (128, 128) 

content = os.listdir(os.getcwd())

# print(content)

images = [item for item in content if os.path.splitext(item)[1].lower() in formats]

for img in images:
    im = Image.open(img)
    try:
        im.resize(size).save('128px_'+img)
    except IOError:
        print('No such files', img)

# Next, find out how to compress images without losing too much resolution