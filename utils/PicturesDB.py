from werkzeug.datastructures import FileStorage
from typing import Union
from uuid import uuid4
from PIL import Image
import shutil
import os


class PicturesDB:
    def __init__(self):
        self.root_path = os.path.split(os.path.abspath(__name__))[0]

        self.database_path = os.path.join(self.root_path, 'pictures')
        if not os.path.exists(self.database_path):
            os.mkdir(self.database_path)
            print('Pictures Database created!')

        self.tables = ['profile-pictures']
        for table in self.tables:
            table_path = os.path.join(self.database_path, table)
            if not os.path.exists(table_path):
                os.mkdir(table_path)
                print('Table', table, 'created!')

    def add_picture(self, table: str, picture: FileStorage) -> Union[bool, tuple]:
        if table not in self.tables:
            print('Table', table, 'not in Tables list!')
            return False

        table_path = os.path.join(self.database_path, table)

        directory_name = uuid4().__str__()
        directory_path = os.path.join(table_path, directory_name)
        os.mkdir(directory_path)

        picture_extension = picture.filename.split('.')[-1]

        picture = Image.open(picture)

        sizes = [256, 128, 64]
        for size in sizes:
            resized_picture = picture.resize((size, size))
            resized_picture.save(os.path.join(directory_path, str(size) + '.' + picture_extension), optimize=True)

        return directory_name, picture_extension

    def get_picture_path(self, table: str, directory_name: str, extension: str, size: int) -> str:
        path = os.path.join(self.database_path, table)
        path = os.path.join(path, directory_name)

        path = os.path.join(path, str(size) + '.' + extension)

        return path

    def delete_picture(self, table: str, directory_path: str):
        path = os.path.join(self.database_path, table)
        path = os.path.join(path, directory_path)

        shutil.rmtree(path)
