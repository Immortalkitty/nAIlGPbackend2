import os
import time
import uuid
import base64
from io import BytesIO
from PIL import Image
from flask import current_app

class FileService:
    def __init__(self, upload_folder, allowed_extensions):
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions

        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder, exist_ok=True)
            with current_app.app_context():
                current_app.logger.info(f"Created upload folder: {self.upload_folder}")

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def save_file(self, file):
        unique_id = uuid.uuid4()
        timestamp = int(time.time())
        _, extension = os.path.splitext(file.filename)
        unique_filename = f"{unique_id}_{timestamp}{extension}"
        filepath = os.path.join(self.upload_folder, unique_filename)

        with current_app.app_context():
            current_app.logger.info(f"Saving file to: {filepath}")

        try:
            file.save(filepath)
            with current_app.app_context():
                current_app.logger.info(f"File saved successfully: {filepath}")
        except Exception as e:
            with current_app.app_context():
                current_app.logger.error(f"Error saving file: {e}")
            raise e

        return unique_filename

    def save_base64_file(self, base64_image, extension=".jpg"):
        unique_id = uuid.uuid4()
        timestamp = int(time.time())
        unique_filename = f"{unique_id}_{timestamp}{extension}"
        filepath = os.path.join(self.upload_folder, unique_filename)


        try:
            image_data = base64.b64decode(base64_image)
            image = Image.open(BytesIO(image_data)).convert('RGB')
            image.save(filepath, format="JPEG")
            with current_app.app_context():
                current_app.logger.info(f"Base64 image saved successfully: {filepath}")
        except Exception as e:
            with current_app.app_context():
                current_app.logger.error(f"Error saving base64 image: {e}")
            raise e

        return unique_filename
