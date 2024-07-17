import requests
from PIL import Image
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import json

with open("./animals.json","r",encoding="utf-8") as jsonfile:
    animals = json.load(jsonfile)

def download_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def apply_mosaic(image, mosaic_size):
    # Convert image to numpy array
    img_array = np.array(image)
    h, w, _ = img_array.shape

    # Create mosaic
    temp_img = img_array.copy()
    for y in range(0, h, mosaic_size):
        for x in range(0, w, mosaic_size):
            temp_img[y:y+mosaic_size, x:x+mosaic_size] = np.mean(temp_img[y:y+mosaic_size, x:x+mosaic_size], axis=(0,1))

    return Image.fromarray(temp_img.astype('uint8'))

for j,animal in enumerate(animals):
    str_j = str(j).zfill(4)
    name = animal["name"]
    imgurl = animal["imgurl"]

    # Download the image
    image = download_image(imgurl)

    # Define mosaic sizes
    mosaic_sizes = [5]
    output_files = [f"./mosaic/{str_j}_mosaic_5.jpg"]

    # Apply mosaic and save files
    for size, output_file in zip(mosaic_sizes, output_files):
        mosaic_image = apply_mosaic(image, size)
        mosaic_image.save(output_file)
        print(f"Saved mosaic image with size {size} to {output_file}")
        print(j)

# Optional: Display the images
# plt.figure(figsize=(15, 5))
# for i, size in enumerate(mosaic_sizes):
#     plt.subplot(1, 4, i + 1)
#     plt.title(f"Mosaic Size: {size}")
#     plt.imshow(apply_mosaic(image, size))
#     plt.axis('off')
# plt.show()
