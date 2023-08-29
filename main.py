import qrcode
from PIL import Image

logo_file_name = 'github-logo.png'
data_to_encode = 'https://github.com/BotsheloRamela/qr-code'

# Create a QRCode instance with the desired size
qr_code = qrcode.QRCode(
    version=1,  # Set the QR code version to 1 (21x21 matrix)
    error_correction=qrcode.constants.ERROR_CORRECT_H
)
qr_code.add_data(data_to_encode)
qr_code.make(fit=True)

# Make a QR code image
qr_code_image = qr_code.make_image().convert('RGB')

# Open and resize the logo image
logo = Image.open(logo_file_name)
logo_resized = logo.resize((80, 80))  # Resize the logo to 80x80 pixels

# Calculate the logo position
logo_x_position = (qr_code_image.size[0] - logo_resized.size[0]) // 2
logo_y_position = (qr_code_image.size[1] - logo_resized.size[1]) // 2
logo_position = (logo_x_position, logo_y_position)

# Paste the logo on the QR code image
qr_code_image.paste(logo_resized, logo_position)

qr_code_image.save('qr_code.png')

print('QR code generated!')