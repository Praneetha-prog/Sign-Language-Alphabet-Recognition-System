import os

IMAGE_FOLDER = "sign_images"

def text_to_sign(text):
    result = []
    text = text.upper()

    for char in text:
        if char.isalpha():

            png_path = os.path.join(IMAGE_FOLDER, f"{char}.png")
            jpg_path = os.path.join(IMAGE_FOLDER, f"{char}.jpg")

            if os.path.exists(png_path):
                result.append((char, png_path))
            elif os.path.exists(jpg_path):
                result.append((char, jpg_path))

    return result