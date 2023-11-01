import os
from typing import List

import cv2
import qrcode

from models import Department

SAVE_DIRECTORY = "test_qrcodes/"
# Ensure the directory exists; if not, create it
if not os.path.exists(SAVE_DIRECTORY):
    os.makedirs(SAVE_DIRECTORY)


def generate_qr_code(user):
    """
    Generate a QR code based on the user's details.
    """
    data = f"{user.name}, {user.department_roles[0].role}, {user.department_roles[0].department.name}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    file_name = f"{user.id}_qr.png"
    img.save(file_name)
    return file_name


def generate_example_qr_codes(users: List[dict]):
    """
    Generate example QR code files for testing.
    """
    for user in users:
        data = f"{user['id']} - {user['name']} - {user['department_role']} - {user['department']}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Construct the file name based on the scenario and save it in the SAVE_DIRECTORY
        file_name = f"{SAVE_DIRECTORY}{user['scenario']}_qr.png"
        img.save(file_name)

        print(f"Saved QR code for {user['name']} as {file_name}")


def decode_qr_codes_from_image(image):
    """
    Decode the multiple QR codes from an image. Not used yet
    """
    decoded_objects = decode(image)
    qr_codes = []

    for obj in decoded_objects:
        data = obj.data.decode("utf-8")
        qr_codes.append(data)

    return qr_codes


def read_qr_code(image_path: str):
    """
    Decode the QR code from an image.
    """
    image = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    value, pts, qr_code = detector.detectAndDecode(image)
    return value
