#!/usr/bin/env python3
import os
from flask import flash
from werkzeug.utils import secure_filename
from api.v1.app import UPLOAD_FOLDER
from datetime import datetime
import json


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MULTI_IMAGE = ('Product', 'Review')
COUNT_IMAGE = 0


def allowed_file(filename: str) -> bool:
    """Check if Extensions is allowed"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_filename(file_extension, id):
    """generate new file name by name id and time"""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    new_filename = f"{COUNT_IMAGE}_{id}_{timestamp}.{file_extension}"
    return new_filename


def rename_file(filename, obj):
    """make new file name"""
    # print(obj)
    file_name = secure_filename(filename)
    file_extension = file_name.rsplit('.', 1)[1].lower()
    # name = f'{obj.first_name}_{obj.last_name}' if type(
    #     obj).__name__ == 'User' else f'{obj.name}'
    return generate_filename(file_extension, obj.id)


def check_directory(obj):
    """check directory if exist else created one"""
    name_class = type(obj).__name__
    if name_class in MULTI_IMAGE:
        directory = f"{os.getcwd()}{UPLOAD_FOLDER}/{name_class}/{name_class}_{obj.id}"
    else:
        directory = f"{os.getcwd()}{UPLOAD_FOLDER}/{name_class}"
    # print(f"\033[33m{os.getcwd()}\033[0m")
    # print(f"\033[33m{directory}\033[0m")
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def deleted_image(method, obj):
    """deleted image for update or delete"""
    name_class = type(obj).__name__
    if name_class in MULTI_IMAGE:
        try:
            images = json.loads(obj.images)
        except json.JSONDecodeError:
            obj.images = None
            obj.save()
            images = {}
    else:
        images = {1: obj.image}
    # print(images)
    for img in images.values():
        old_img = os.path.join(f"{os.getcwd()}/api/v1/static", img[1:])
        if os.path.exists(old_img):
            os.remove(old_img)
    if method == 'DELETE':
        folder = f"{os.getcwd()}/api/v1/static/uploads/{name_class}/{name_class}_{obj.id}"
        if os.path.exists(folder):
            os.rmdir(folder)


def upload_image(request, obj):
    """methods that upload image to the server"""
    global COUNT_IMAGE
    name_class = type(obj).__name__
    if 'file' in request.files:
        # file = request.files['file']
        # print("*", request.files['file'])
        files = request.files.getlist('file')
        print("**", files)
        files_path = {}
        for file in files:
            print("***", file)

            if len(file.filename):
                if file and allowed_file(file.filename):
                    directory = check_directory(obj)
                    file_name = rename_file(file.filename, obj)
                    full_path = os.path.join(directory, file_name)
                    file.save(full_path)

                    if name_class in MULTI_IMAGE:
                        files_path[COUNT_IMAGE] = f"/uploads/{name_class}/{name_class}_{obj.id}/{file_name}"
                        COUNT_IMAGE += 1
                    else:
                        files_path[COUNT_IMAGE] = f"/uploads/{name_class}/{file_name}"
                        break
                    # return True
                    # print('image saved')
                else:
                    continue
        print(f"__ {files_path} __")
        if request.method == 'PUT':
            deleted_image('PUT', obj)
        if name_class in MULTI_IMAGE:
            obj.images = json.dumps(files_path, indent=2)
        else:
            obj.image = files_path[0]
        obj.save()
        COUNT_IMAGE = 0
