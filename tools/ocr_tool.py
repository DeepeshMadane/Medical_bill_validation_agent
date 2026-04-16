import pytesseract
from PIL import Image
import cv2

def preprocess(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    return thresh
def extract_text(image_path):
    text = pytesseract.image_to_string(preprocess(image_path))
    return text