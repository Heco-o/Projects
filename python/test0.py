import pytesseract
from PIL import Image
import requests
import re

url = "output_image.jpg"
# Open the image file
#image = Image.open(requests.get(url, stream=True).raw)
image = Image.open(url)

# Perform OCR using PyTesseract
text = pytesseract.image_to_string(image)
text = re.sub(r'[^a-zA-Z ]', '', text).split(" ")

# Print the extracted text
print(text)