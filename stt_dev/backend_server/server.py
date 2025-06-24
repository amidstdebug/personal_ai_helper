# file_utils.py

import os
import shutil
from utils.logger import get_logger

logger = get_logger("file_utils")

def save_upload_file(file, target_path: str):
    try:
        with open(target_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"Saved file to {target_path}")
    except Exception as e:
        logger.exception(f"Failed to write file: {target_path}")
        raise

def delete_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
            logger.info(f"Deleted file: {path}")
    except Exception as e:
        logger.warning(f"Failed to delete file {path}: {e}")