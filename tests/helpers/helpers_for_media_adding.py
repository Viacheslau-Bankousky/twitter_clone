"""
This module contains functions for preparing media content for testing.

During testing, we need to prepare media content for upload.
It essentially reads an image file and converts the content into bytes
and additionally provides the filename and file type.

Uses:
-----
- `aiofiles` for asynchronous file operations.
- `typing` for type hinting.

"""

from typing import Dict, Tuple

import aiofiles


async def make_media_content() -> Dict[str, Tuple[str, bytes, str]]:
    """
    Read an image file and return its bytes' content.

    Returns:
        media_content (Dict[str, Tuple[str, bytes, str]]):
            A dictionary containing name of file,
            corresponding byte content and file type.

    """
    async with aiofiles.open(
        "../../twitter_clone_logo.jpg",
        "rb",
    ) as file_object:
        media_byte_str: bytes = await file_object.read()
        media_content: Dict[str, Tuple[str, bytes, str]] = {
            "file": ("twitter_clone_logo.jpg", media_byte_str, "image/jpeg"),
        }
    return media_content


async def make_wrong_media_content(
    file_path: str, file_type: str,
) -> Dict[str, Tuple[str, bytes, str]]:
    """
    Read a fake media file and return its bytes content.

    This function can handle file types other than JPG images.

    Args:
        file_path (str):
            Path to file
        file_type (str):
            File type

    Returns:
        media_content (Dict[str, Tuple[str, bytes, str]]):
            A dictionary containing name of file, corresponding byte
            content and file type.
    """
    async with aiofiles.open(
        file_path,
        "rb",
    ) as file_object:
        media_byte_str: bytes = await file_object.read()
        media_content: Dict[str, Tuple[str, bytes, str]] = {
            "file": (file_path.split("/")[-1], media_byte_str, file_type),
        }
    return media_content
