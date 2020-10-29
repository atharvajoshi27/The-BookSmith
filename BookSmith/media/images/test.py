from PIL import Image
filename = 'image_5.jpeg'
im = Image.open(filename)
print(im.size)
im = im.resize((700, 700), Image.ANTIALIAS)
print(im.size)
quality_val = 100
im.save(filename, quality=quality_val)
