from PIL import Image
from PIL.ExifTags import TAGS

def extract_metadata(image_path):
    image = Image.open(image_path)
    info = image._getexif()
    
    if not info:
        return "No metadata available"
    
    metadata = {}
    for tag, value in info.items():
        tag_name = TAGS.get(tag, tag)
        metadata[tag_name] = value
    
    return metadata
