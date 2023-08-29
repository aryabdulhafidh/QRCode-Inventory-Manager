import qrcode
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import random
import string

# Constants
LOGO_SIZE = (80, 80)
QR_VERSION = 1
LOGO_FILE_NAME = 'github-logo.png'
OUTPUT_PDF = 'qr_codes.pdf'

def generate_item_code():
    """"Generate a random 6-character code"""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

def generate_qr_code_with_logo(item_id, qr_canvas):
    """"Create a QRCode instance with the desired size"""
    qr_code = qrcode.QRCode(
        version=QR_VERSION,
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )

    # Generate a unique item code
    item_code = generate_item_code()

    # Combine item ID and item code for QR code data
    data_to_encode = f'Item ID: {item_id}\nItem Code: {item_code}'
    qr_code.add_data(data_to_encode)
    qr_code.make(fit=True)

    # Make a QR code image
    qr_code_image = qr_code.make_image().convert('RGB')

    try:
        # Open and resize the logo image
        logo_path = os.path.join(os.getcwd(), LOGO_FILE_NAME)
        logo = Image.open(logo_path)
        logo_resized = logo.resize(LOGO_SIZE)

        # Calculate the logo position
        logo_x_position = (qr_code_image.size[0] - logo_resized.size[0]) // 2
        logo_y_position = (qr_code_image.size[1] - logo_resized.size[1]) // 2
        logo_position = (logo_x_position, logo_y_position)

        # Paste the logo on the QR code image
        qr_code_image.paste(logo_resized, logo_position)

        # Draw the QR code image on the PDF canvas
        qr_canvas.drawInlineImage(qr_code_image, 100, 500 - (item_id - 1) * 150, width=300, height=300)

    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    c = canvas.Canvas(OUTPUT_PDF, pagesize=letter)
    num_items = 10  # Number of QR codes to generate

    for item_id in range(1, num_items + 1):
        generate_qr_code_with_logo(item_id, c)

    c.save()
    print(f'QR codes saved in {OUTPUT_PDF}!')