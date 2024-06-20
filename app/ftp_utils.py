# ftp_utils.py

import ftplib

from django.conf import settings

FTP_HOST = settings.FTP_HOST
FTP_PORT = settings.FTP_PORT
FTP_USER = settings.FTP_USER
FTP_PASS = settings.FTP_PASS


class FTPClient:
    def __init__(self):
        self.ftp = ftplib.FTP()

    def __enter__(self):
        self.ftp.connect(FTP_HOST, FTP_PORT)
        self.ftp.login(FTP_USER, FTP_PASS)
        return self.ftp

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ftp.quit()


def upload_file(local_file_path, remote_file_path):
    with FTPClient() as ftp:
        with open(local_file_path, "rb") as file:
            ftp.storbinary(f"STOR {remote_file_path}", file)


def download_file(remote_file_path, local_file_path):
    with FTPClient() as ftp:
        with open(local_file_path, "wb") as file:
            ftp.retrbinary(f"RETR {remote_file_path}", file.write)
