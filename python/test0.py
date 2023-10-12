import pytesseract
from PIL import Image
import requests
import re

url = "https://cdn.discordapp.com/attachments/1161913417259552789/1162070731899805706/prediction.png?ex=653a99b4&is=652824b4&hm=cadf5ca50bee014eb4b37068a2f08ebd690b02ea9ab61e9f2dc28729a5edfd40&"
# Open the image file
image = Image.open(requests.get(url, stream=True).raw)

# Perform OCR using PyTesseract
text = pytesseract.image_to_string(image)
text = re.sub(r'[^a-zA-Z ]', '', text).split(" ")

# Print the extracted text
print(text[0])