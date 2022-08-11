from PIL import Image, ImageGrab
from pytesseract import *

print(pytesseract.image_to_string(ImageGrab.grabclipboard()))