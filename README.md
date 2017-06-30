# Upload Test
Automatically reads a scanned image of an Ontario G driver's license

Parses out the driver's name and license number

Fills in each of the 4 insurance documents with the driver's full name and driver's license number where applicable.

4 insurance documents are downloadable

## Documentation

Install prerequisites:

    pip install django
    pip install pytesseract
    apt-get install tesseract-ocr
    pip install python-docx

Then run:

    cd upload-test/mysite
    python manage.py runserver

It start should running the server with the line (or similar):

    Starting development server at http://127.0.0.1:8000/

Log into http://127.0.0.1:8000/ to go to the main page.

Change address to http://127.0.0.1:8000/admin

Log into the admin account with credentials: ``han.solo/password123``

Click ``Upload License`` and add/upload the images in ``upload-test/test_images/``

Downloads can be done in admin->Upload Licence page

### Limitations

Images parsing code was tweaked for images in ``upload-test/test_images/``.  Adding other scanned images may break it.

## Environment
Developed with Python 2.7.12

Developed on Ubuntu 16.04.2
