import qrcode
from PIL import Image
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
import os
import random
import string
import math

# Constants
LOGO_SIZE = (80, 80)
QR_SIZE = (80, 80)
QR_VERSION = 1
LOGO_FILE_NAME = 'github-logo.png'
OUTPUT_PDF = 'QR_Codes.pdf'
DEFAULT_COLUMN_SIZE = 8

def generate_item_code():
    """"Generate a random 6-character code"""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

def generate_qr_code_with_logo(item_id, qr_canvas, num_columns, x_position, y_position):
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

        # Calculate row and column for current QR code
        # row = (item_id - 1) // total_columns
        # column = (item_id - 1) % total_columns
        # x_position = 10 + column * (QR_SIZE[0] + 20)
        # y_position = A4[1] - 40 - row * (QR_SIZE[1] + 10) - QR_SIZE[1]

        # Draw the QR code image on the PDF canvas
        qr_canvas.drawInlineImage(qr_code_image, x_position, y_position, width=QR_SIZE[0], height=QR_SIZE[1])


    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    c = canvas.Canvas(OUTPUT_PDF, pagesize=A4) 
    num_items = 32  # Number of items to generate QR codes for (6 columns x 7 rows)
    num_columns = DEFAULT_COLUMN_SIZE
    
    # Calculate the number of full rows and the remaining items for the last row
    num_full_columns = num_items // num_columns
    remaining_items = num_items % num_columns


    for column in range(num_full_columns):
        for row in range(num_columns):
            item_id = column * num_columns + row + 1

            x_position = 20 + column * (QR_SIZE[0] + 20)
            y_position = A4[1] - 40 - row * (QR_SIZE[1] + 20) - QR_SIZE[1]

            generate_qr_code_with_logo(item_id, c, num_columns, x_position, y_position)

    # Generate the last column
    for row in range(remaining_items):
        item_id = num_full_columns * num_columns + row + 1

        x_position = 20 + num_full_columns * (QR_SIZE[0] + 20)
        y_position = A4[1] - 40 - row * (QR_SIZE[1] + 20) - QR_SIZE[1]

        generate_qr_code_with_logo(item_id, c, num_columns, x_position, y_position)


    c.save()
    print(f'QR codes saved in {OUTPUT_PDF}!')