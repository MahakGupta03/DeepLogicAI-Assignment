from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import csv

def extract_text_from_pdf(pdf_path):
    pytesseract.pytesseract.tesseract_cmd ='C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    # Convert the PDF to PIL image
    image = convert_from_path(pdf_path, single_file=True)[0]
    image.save('output_image.png', 'PNG')
    text = extract_text_from_image('output_image.png')
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


def save_to_csv(header_data, csv_path):
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write header data to CSV
        for key, value in header_data.items():
            writer.writerow([key, value])
        

file_path = input("Enter complete path of file: ")  #Example -> C:\\Users\\yashh\\Downloads\\Sample Files\\sample2.pdf
file_text=""
if (file_path.lower().endswith('.pdf')):
    file_text = extract_text_from_pdf(file_path)
elif(file_path.lower().endswith(('.png', '.jpg', '.jpeg'))):
    file_text = extract_text_from_image(file_path)

csv_path = "extracted_data.csv"

key_value_pair = extract_key_value_pairs(file_text)

save_to_csv(key_value_pair, csv_path)
