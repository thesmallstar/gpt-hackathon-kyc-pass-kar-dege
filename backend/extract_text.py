import pytesseract
import string
import os

import os
import io
from pdf2image import convert_from_path

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/manuj.v/Desktop/key.json"

import io
from google.cloud import vision



def google_vision_data(image_path):
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    document = response.full_text_annotation.text

    return document

def extract_text_using_tesseract(path):
    text = pytesseract.image_to_string(path)
    return text


def clean_text(text):
    text_clean = "".join([i for i in text if i not in string.punctuation])
    return text_clean


def cleaned_text_from_image(path):
    text = google_vision_data(path)
    cleaned_text = clean_text(text)
    return cleaned_text


def cleaned_text_from_pdf(path):

    output_dir = "../../documents"
    # Create output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)
    image_arr = []

    os.makedirs(output_dir, exist_ok=True)

    # Convert PDF pages to Pillow Image objects
    images = convert_from_path(path, 300)  # 300 is the resolution

    # Save the images to the output directory
    for i, image in enumerate(images):
        image.save(os.path.join(output_dir, f'page_{i + 1}.jpg'), 'JPEG')
        saved_image_name = f"page_{i + 1}.jpg"
        image_arr.append(os.path.join(output_dir, saved_image_name))

    cleaned_text = ""
    for doc in image_arr:
        text = cleaned_text_from_image(doc)
        cleaned_text = cleaned_text + text

    return cleaned_text
