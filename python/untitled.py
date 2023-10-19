import cv2
import numpy as np
import requests
from PIL import Image
from io import BytesIO
import time

# URL of the image
image_url = "https://media.discordapp.net/attachments/1161913417259552789/1162142071461781625/prediction.png?ex=653adc25&is=65286725&hm=518a14809aa160954729673a3cc5f1fb5b4c784d01356554c0509a7e95f9ba90&"

# Download the image from the URL
response = requests.get(image_url)
s = time.time()
image_bytes = BytesIO(response.content)

# Load the image
image = cv2.imdecode(np.frombuffer(image_bytes.read(), np.uint8), cv2.IMREAD_COLOR)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold the grayscale image to isolate the black text
_, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# Invert the thresholded image to make the black text white
thresholded = cv2.bitwise_not(thresholded)

# Create a white background image
white_background = np.ones_like(image) * 255

# Combine the white background with the black text
result = cv2.bitwise_or(image, image, mask=thresholded)
result_on_white = cv2.bitwise_or(white_background, white_background, mask=cv2.bitwise_not(thresholded))

# Combine the result with the white background
final_result = cv2.bitwise_or(result_on_white, result)

# Save the final image
cv2.imwrite('output_image.jpg', final_result)
print(time.time() - s)