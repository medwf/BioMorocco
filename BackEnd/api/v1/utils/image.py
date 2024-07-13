#!/usr/bin/env python3
import os
from flask import flash
from werkzeug.utils import secure_filename
from api.v1.app import UPLOAD_FOLDER
from datetime import datetime


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename: str) -> bool:
    """Check if Extensions is allowed"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_filename(file_extension, name, id):
    """generate new file name by name id and time"""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    new_filename = f"{name}_{id}_{timestamp}.{file_extension}"
    return new_filename


def rename_file(filename, obj):
    """make new file name"""
    file_name = secure_filename(filename)
    file_extension = file_name.rsplit('.', 1)[1].lower()
    name = f'{obj.first_name}_{obj.last_name}' if type(
        obj).__name__ == 'User' else f'{obj.name}'
    return generate_filename(file_extension, name, obj.id)


def check_directory(obj):
    """check directory if exist else created one"""
    directory = f"{os.getcwd()}{UPLOAD_FOLDER}/{type(obj).__name__}"
    # print(f"\033[33m{os.getcwd()}\033[0m")
    # print(f"\033[33m{directory}\033[0m")
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def deleted_image(obj):
    """deleted image for update or delete"""
    old_img = os.path.join(
        f"{os.getcwd()}/api/v1/static", obj.image[1:])
    # print("**", old_img)
    if os.path.exists(old_img):
        os.remove(old_img)


def upload_image(request, obj):
    """methods that upload image to the server"""
    if 'file' in request.files:
        file = request.files['file']

        if len(file.filename):
            if file and allowed_file(file.filename):
                directory = check_directory(obj)
                file_name = rename_file(file.filename, obj)
                full_path = os.path.join(directory, file_name)

                if request.method == 'PUT' and obj.image:
                    deleted_image(obj)

                file.save(full_path)
                obj.image = f"/uploads/{type(obj).__name__}/{file_name}"
                obj.save()
                return True
                # print('image saved')
        # print('No selected file')
    # print('No file part')
    return False
