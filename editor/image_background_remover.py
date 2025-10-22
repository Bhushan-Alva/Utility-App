from PIL import Image
import os

try:
    from rembg import remove  # AI-based background removal
    rembg_available = True
except ImportError:
    rembg_available = False


class ImageBackgroundRemover:
    def __init__(self, input_path=None, output_path=None, mode='simple', bg_color=(255, 255, 255)):
        """
        :param input_path: path to input image
        :param output_path: folder to save output
        :param mode: 'simple' or 'complex'
        :param bg_color: background color for simple mode (R, G, B)
        """
        self.input_path = input_path
        self.output_path = output_path
        self.mode = mode.lower()
        self.bg_color = bg_color

    def remove_background(self):
        if not os.path.exists(self.input_path):
            print("❌ Input file not found.")
            return

        # Open image
        with Image.open(self.input_path) as img:
            output_file = os.path.join(self.output_path, "background_removed.png")

            if self.mode == 'complex':
                if not rembg_available:
                    print("⚠️ rembg not installed. Run: pip install rembg onnxruntime")
                    return
                print("🧠 Using AI-based background removal...")
                result = remove(img)
                result.save(output_file)

            elif self.mode == 'simple':
                print("⚡ Using simple color-based background removal...")
                img = img.convert("RGBA")
                datas = img.getdata()

                new_data = []
                for item in datas:
                    # Example logic: treat near-white pixels as background
                    if item[0] > 200 and item[1] > 200 and item[2] > 200:
                        new_data.append((255, 255, 255, 0))  # transparent
                    else:
                        new_data.append(item)

                img.putdata(new_data)
                img.save(output_file)

            print(f"✅ Background removed → {output_file}")
            return output_file


# # Example Usage
# simple_removal = ImageBackgroundRemover(
#     input_path=r"C:\Users\bhush\OneDrive\Desktop\Barn\Utility App\test\converted_image.jpg",
#     output_path=r"C:\Users\bhush\OneDrive\Desktop\Barn\Utility App\test",
#     mode='simple'
# )
# simple_removal.remove_background()


complex_removal = ImageBackgroundRemover(
    input_path=r"C:\Users\bhush\OneDrive\Desktop\Barn\Utility App\test\converted_image.jpg",
    output_path=r"C:\Users\bhush\OneDrive\Desktop\Barn\Utility App\test",
    mode='complex'
)
complex_removal.remove_background()
