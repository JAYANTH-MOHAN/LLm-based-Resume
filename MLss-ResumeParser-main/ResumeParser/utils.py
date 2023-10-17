
import os
import sys
import aiofiles
from typing import Optional, Tuple, Union
from pathlib import Path
from datetime import datetime
from fastapi import UploadFile


def get_file_name(store_folder, ext) -> tuple:

    if os.path.exists(store_folder):
        pass
    else:
        os.makedirs(store_folder)

    current_datetime = datetime.now()
    str_current_datetime = str(current_datetime)
    timestamp = str_current_datetime.replace(" ", "_")
    file_name = timestamp + "." + ext
    file_name = os.path.join(str(store_folder), file_name)
    return file_name, timestamp


def delete_file(filepath: Union[str, Tuple[str, Optional[str]]]) -> None:
    """
    Delete a file or a list of files.

    Args:
        filepath (Union[str, Tuple[str]]): Path to the file to delete.
    """
    if isinstance(filepath, str):
        filepath = (filepath, None)

    for path in filepath:
        if path:
            Path(path).unlink(missing_ok=True)


def retrieve_user_platform() -> str:
    """
    Retrieve the user's platform.

    Returns:
        str: User's platform. Either 'linux', 'darwin' or 'win32'.
    """
    return sys.platform


async def save_file_locally(filename: str, file: "UploadFile") -> bool:
    """
    Save a file locally from an UploadFile object.

    Args:
        filename (str): The filename to save the file as.
        file (UploadFile): The UploadFile object.

    Returns:
        bool: Whether the file was saved successfully.
    """
    async with aiofiles.open(filename, "wb") as f:
        file_bytes = await file.read()
        await f.write(file_bytes)

    return True



