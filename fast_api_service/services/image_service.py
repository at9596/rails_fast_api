from PIL import Image, ImageFilter
import io

class ImageService:
    @staticmethod
    def apply_gaussian_blur(image_bytes: bytes, radius: int = 15) -> bytes:
        # Open image from bytes
        img = Image.open(io.BytesIO(image_bytes))

        # Apply the filter
        processed_img = img.filter(ImageFilter.GaussianBlur(radius=radius))

        # Save to byte array
        img_byte_arr = io.BytesIO()
        processed_img.save(img_byte_arr, format="PNG")
        
        return img_byte_arr.getvalue()