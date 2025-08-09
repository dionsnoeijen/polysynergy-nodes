from typing import TypedDict, Dict, Any


class Image(TypedDict):
    """Type definition for image objects used throughout the image processing nodes"""
    url: str
    mime_type: str
    width: int
    height: int
    size: int
    metadata: Dict[str, Any]