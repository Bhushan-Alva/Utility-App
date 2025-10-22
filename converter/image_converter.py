from PIL import Image
import os

class ImageConverter:
    TYPES = ['JPEG', 'PNG', 'BMP', 'ICO', 'WEBP', 'TIFF']

    def __init__(self, input_path=None, output_path=None, output_format=None, quality=90, bg_color=(255, 255, 255)):
        self.input_path = input_path
        self.output_path = output_path
        self.output_format = output_format
        self.quality = quality
        self.bg_color = bg_color  # For PNG -> JPEG conversion

        # Map user input to Pillow format names (typo-safe)
        self.format_map = {k.upper(): v for k, v in {
            'JPG':'JPEG', 'JPEG':'JPEG', 'PNG':'PNG', 'BMP':'BMP', 
            'ICO':'ICO', 'WEBP':'WEBP', 'TIFF':'TIFF'
        }.items()}

        if self.output_path:
            os.makedirs(self.output_path, exist_ok=True)

    def convert_image(self, img_path):
        user_fmt = self.output_format.upper()
        if user_fmt not in self.format_map:
            print(f"Unsupported format: {self.output_format}")
            return

        pillow_format = self.format_map[user_fmt]

        try:
            with Image.open(img_path) as img:
                # Handle PNG/LA -> JPEG transparency
                if pillow_format == 'JPEG' and img.mode in ('RGBA', 'LA'):
                    if img.mode == 'RGBA':
                        background = Image.new("RGB", img.size, self.bg_color)
                        alpha = img.split()[3]
                    else:  # LA mode
                        background = Image.new("L", img.size, self.bg_color[0])
                        alpha = img.split()[1]
                    background.paste(img, mask=alpha)
                    img = background
                elif pillow_format == 'JPEG' and img.mode not in ('RGB', 'L'):
                    img = img.convert('RGB')
                elif pillow_format != 'JPEG' and img.mode not in ('RGB', 'RGBA', 'L'):
                    img = img.convert('RGB')

                # Output filename
                filename = os.path.splitext(os.path.basename(img_path))[0]
                output_file = os.path.join(self.output_path, f"{filename}_converted.{pillow_format.lower()}")

                # Save image
                img.save(output_file, format=pillow_format, quality=self.quality)
                print(f"✅ Converted: {img_path} → {output_file}")
        except Exception as e:
            print(f"❌ Error converting {img_path}: {e}")

    def convert_all(self):
        """Convert a single image or all images in a folder."""
        if os.path.isfile(self.input_path):
            self.convert_image(self.input_path)
        elif os.path.isdir(self.input_path):
            for file in os.listdir(self.input_path):
                file_path = os.path.join(self.input_path, file)
                if os.path.isfile(file_path) and file.lower().endswith(tuple(['.jpg','.jpeg','.png','.bmp','.ico','.webp','.tiff'])):
                    self.convert_image(file_path)
        else:
            print("Invalid input path.")


# ------------------- Example Usage -------------------

# Single image conversion
image = ImageConverter(
    input_path=r'C:\Users\bhush\OneDrive\Desktop\Barn\Utility App\converter\a_converted_converted.jpeg',
    output_path=r'C:\Users\bhush\OneDrive\Desktop\Barn\Utility App\converter\output',
    output_format='png',  # typo-safe mapping
    bg_color=(124, 126, 255)  # background for JPEG transparency
)
image.convert_all()

# Folder conversion
folder_converter = ImageConverter(
    input_path=r'C:\Users\bhush\OneDrive\Desktop\Barn\Utility App\converter\input_folder',
    output_path=r'C:\Users\bhush\OneDrive\Desktop\Barn\Utility App\converter\output',
    output_format='jpg',  
    bg_color=(255, 255, 255)
)
folder_converter.convert_all()
