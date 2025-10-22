from PIL import Image
import os

class ImageCompressor:
    TYPES = ['JPEG', 'PNG', 'BMP', 'ICO', 'WEBP', 'TIFF']

    def __init__(self, input_path=None, output_path=None, quality=85, max_width=None, max_height=None):
        """
        :param input_path: path to the input image
        :param output_path: folder to save compressed image
        :param quality: compression quality for JPEG/WebP (0-100)
        :param max_width: optional max width to resize
        :param max_height: optional max height to resize
        """
        self.input_path = input_path
        self.output_path = output_path
        self.quality = quality
        self.max_width = max_width
        self.max_height = max_height

    def compress_image(self):
        # Open image
        with Image.open(self.input_path) as img:
            original_format = img.format

            # Resize if needed
            if self.max_width or self.max_height:
                width, height = img.size
                scale = 1.0

                if self.max_width and width > self.max_width:
                    scale = min(scale, self.max_width / width)
                if self.max_height and height > self.max_height:
                    scale = min(scale, self.max_height / height)

                if scale < 1.0:
                    new_size = (int(width * scale), int(height * scale))
                    img = img.resize(new_size, resample=Image.Resampling.LANCZOS)

            # Build dynamic output filename
            filename = os.path.splitext(os.path.basename(self.input_path))[0]
            output_file = os.path.join(self.output_path, f"{filename}_compressed.{original_format.lower()}")

            # Save with compression
            save_params = {}
            if original_format in ['JPEG', 'JPG', 'WEBP']:
                save_params['quality'] = self.quality
                save_params['optimize'] = True
            elif original_format == 'PNG':
                save_params['optimize'] = True  # PNG compression

            # Preserve transparency for PNG/WebP
            if original_format in ['PNG', 'WEBP'] and img.mode not in ('RGBA', 'LA'):
                img = img.convert('RGBA')

            img.save(output_file, format=original_format, **save_params)
            print(f"Image compressed successfully → {output_file}")

            return output_file
        





# Compress an already converted image
compressed_file = ImageCompressor(
    input_path=r"C:\Users\bhush\OneDrive\Desktop\Barn\Utility App\test\a_converted.bmp",
    output_path=r"C:\Users\bhush\OneDrive\Desktop\Barn\Utility App\test",
    quality=30,          # JPEG/WebP quality
    max_width=1024,      # optional resizing
    max_height=1024
).compress_image()
