import os
import uuid
import shutil
import zipfile
import tarfile


UPLOAD_DIR = "uploads"
EXTRACT_DIR = "extracted"


class FileUtils:

    @staticmethod
    def save_upload(upload_file):

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        unique_name = (
            str(uuid.uuid4())
            + "_"
            + upload_file.filename
        )

        file_path = os.path.join(
            UPLOAD_DIR,
            unique_name
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                upload_file.file,
                buffer
            )

        return file_path

    @staticmethod
    def extract_archive(file_path):

        os.makedirs(
            EXTRACT_DIR,
            exist_ok=True
        )

        extract_path = os.path.join(
            EXTRACT_DIR,
            os.path.basename(file_path)
        )

        os.makedirs(
            extract_path,
            exist_ok=True
        )

        if file_path.endswith(".zip"):

            with zipfile.ZipFile(file_path) as z:
                z.extractall(extract_path)

        elif (
            file_path.endswith(".tar")
            or
            file_path.endswith(".tar.gz")
            or
            file_path.endswith(".tgz")
        ):

            with tarfile.open(file_path) as t:
                t.extractall(extract_path)

        else:
            raise Exception("Unsupported archive")

        return extract_path