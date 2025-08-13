from PIL import Image, ImageChops, ImageEnhance

def convert_to_ela_image(image_path, quality):
    original_image = Image.open(image_path)
    ela_image_path = image_path.split('.')[0] + "_ela.jpg"
    original_image.save(ela_image_path, 'JPEG', quality=quality)
    
    ela_image = Image.open(ela_image_path)
    diff = ImageChops.difference(original_image, ela_image)
    
    extrema = diff.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    
    scale = 255.0 / max_diff if max_diff != 0 else 1
    
    diff = ImageEnhance.Brightness(diff).enhance(scale)
    
    return diff
