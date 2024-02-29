from django.shortcuts import render, HttpResponse
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import cv2
import os

def extract_table_from_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    custom_config = r'--oem 3 --psm 6'
    table_data = pytesseract.image_to_string(gray, config=custom_config)
    return table_data

def extract_text_from_pdf(pdf_path):
    pytesseract.pytesseract.tesseract_cmd ='C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    # Convert the PDF to PIL image
    image = convert_from_path(pdf_path, single_file=True)[0]
    image.save('output_image.png', 'PNG')
    text = extract_table_from_image('output_image.png')
    return text

def extract_text_from_image(image_path):
    pytesseract.pytesseract.tesseract_cmd ='C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_key_value_pairs(text):
    key_value_pairs = {}
    lines = text.split('\n')
    for line in lines:
        # Split the line into key and value assuming a tab or colon separator
        parts = line.split(':') or line.split('\t')
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()
            key_value_pairs[key] = value
        elif len(parts[0]) >0 and len(parts) != 2:
            length = len(parts[0])
            key = parts[0][:(int)(length/2)]
            value = parts[0][(int)(length/2):]
            key_value_pairs[key] = value

    return key_value_pairs


def upload_file(request):
    if request.method == 'POST':
        file_name = request.FILES.get('file')
        fss = FileSystemStorage()
        file = fss.save(file_name.name, file_name)
        total_path = os.path.join(settings.BASE_DIR,settings.MEDIA_ROOT)+ '\\' + str(file_name)
        input_file = ""
        if('.pdf' in file_name.name):
            input_file = extract_text_from_pdf(total_path)
        elif(file_name.name.lower().endswith(('.png', '.jpg', '.jpeg'))):
            input_file = extract_text_from_image(total_path)
        else:
            return HttpResponse("File should be either pdf or image")
        key_value_data = extract_key_value_pairs(input_file)
        return render(request, 'result.html', {'key_value_data': key_value_data})
    return render(request, 'upload.html')
