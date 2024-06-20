# ftp_utils.py

import ftplib
import logging

from django.conf import settings

FTP_HOST = settings.FTP_HOST
FTP_PORT = settings.FTP_PORT
FTP_USER = settings.FTP_USER
FTP_PASS = settings.FTP_PASS

# Configure logging
logger = logging.getLogger(__name__)


class FTPClient:
    def __init__(self):
        self.ftp = ftplib.FTP()

    def __enter__(self):
        try:
            self.ftp.connect(FTP_HOST, FTP_PORT)
            self.ftp.login(FTP_USER, FTP_PASS)
            return self.ftp
        except ftplib.all_errors as e:
            logger.error(f"FTP connection error: {str(e)}")
            raise Exception(f"FTP connection error: {str(e)}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ftp.quit()


def upload_file(local_file_path, remote_file_path):
    with FTPClient() as ftp:
        try:
            with open(local_file_path, "rb") as file:
                ftp.storbinary(f"STOR {remote_file_path}", file)
                logger.info(
                    f"Uploaded file '{local_file_path}' to '{remote_file_path}'"
                )
        except ftplib.all_errors as e:
            logger.error(f"FTP upload error: {str(e)}")
            raise Exception(f"FTP upload error: {str(e)}")


def download_file(remote_file_path, local_file_path):
    with FTPClient() as ftp:
        try:
            with open(local_file_path, "wb") as file:
                ftp.retrbinary(f"RETR {remote_file_path}", file.write)
                logger.info(
                    f"Downloaded file '{remote_file_path}' to '{local_file_path}'"
                )
        except ftplib.all_errors as e:
            logger.error(f"FTP download error: {str(e)}")
            raise Exception(f"FTP download error: {str(e)}")
