#/usr/bin/env python

from docx import Document
from datetime import datetime
from django.conf import settings

import pytesseract
import re
import os

try:
    import Image
except ImportError:
    from PIL import Image

def fill_docs(driver_info, uploaded_image):
    """Fill out the four insurance documents with the parsed info"""

    destination_filename = str(uploaded_image).split('/')[-1][:-4]

    path_template = ('{}/application/insurance_template/'
                     .format(settings.BASE_DIR))
    path_destination = ('{}/application/media/upload_license/'
                       .format(settings.BASE_DIR))

    doc_template = ['Insurance_permit-1.docx','Insurance_permit-2.docx',
                    'Insurance_permit-3.docx','Insurance_permit-4.docx']

    string_name = "Driver Name:"
    string_license = "Drivers licence no:"
    info_doc = []
    for i in doc_template:
        document = Document(path_template+i)
        for p in document.paragraphs:
            if string_name in p.text:
                p.text = '{} {}'.format(string_name,
                                        ' '.join(driver_info[1][::-1]))
            elif string_license in p.text:
                p.text = '{} {}'.format(string_license,
                                        driver_info[2].replace(' ',''))
            elif '<date>' in p.text:
                p.text = datetime.now().strftime('%d %b, %Y')

        save_doc = i.replace('.docx','_{}_{}.docx'
                .format(('_'.join(driver_info[1][::-1]))
                        ,destination_filename))
        document.save(path_destination+save_doc)
        info_doc.append(save_doc)

    return info_doc


def parse_name_number(string):
    """re search for and returns Drivers License, Name, and License no"""

    regex_license = r"Driver\W*s Licence"
    regex_name = (r'[A-Z]*\s*[A-Z]+\W*\s+[A-Z]+\s+[0-9]'
                  '+\s+[A-Z]+\s+[A-Z]+\s+[A-Z]+\W*\s+ON')
    regex_number = r'[A-Z]\d{4}\s*-*\s*\d{5}\s*-*\s*\d{5}'

    driver_info = []
    string = string.encode('ascii', 'ignore')

    match = re.search(regex_license, string)

    if match:
        driver_info += [match.group()]
    match = re.search(regex_name, string)
    if match:
        driver_info += [filter(None, match.group().strip().split('\n'))[:2]]
    match = re.search(regex_number, string)
    if match:
        driver_info += [match.group()]

    return driver_info


def parse_license(image):
    """Turns image to text.  Returns all text found"""

    img = Image.open(image)
    width = img.width
    height = img.height

    for w in range(width):
        for h in range(height):
            pixel = img.getpixel((w, h))
            if pixel[0] < 120 and pixel[1] < 90 and pixel[2] < 105:
                img.putpixel((w,h), (0,0,0))
            else:
                img.putpixel((w,h), (255,255,255))
    return pytesseract.image_to_string(img)


def handle(uploaded_image):

    parsed_license = parse_license(uploaded_image)
    if parsed_license:
        driver_info = parse_name_number(parsed_license)
    if driver_info and len(driver_info) == 3:
        return fill_docs(driver_info, uploaded_image)
