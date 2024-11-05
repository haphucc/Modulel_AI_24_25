import os
from PIL import Image, ImageEnhance

# Hàm để tăng độ sáng và chi tiết cho ảnh
def enhance_image(image_path, output_path):
    # Mở ảnh
    img = Image.open(image_path)

    # Tăng độ sáng (hệ số 1.5 có thể điều chỉnh)
    enhancer_brightness = ImageEnhance.Brightness(img)
    img_brightened = enhancer_brightness.enhance(1.5)

    # Tăng chi tiết (hệ số 2 có thể điều chỉnh)
    enhancer_sharpness = ImageEnhance.Sharpness(img_brightened)
    img_enhanced = enhancer_sharpness.enhance(10)

    # Lưu ảnh đã chỉnh sửa
    img_enhanced.save(output_path)

# Hàm duyệt qua tất cả các ảnh trong thư mục và áp dụng tăng độ sáng và chi tiết
def process_images_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".JPG"):
            image_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            print(f"Processing {filename}...")

            # Tăng độ sáng và chi tiết cho ảnh
            enhance_image(image_path, output_path)

# Thư mục chứa ảnh đầu vào và đầu ra
input_folder = "data/Goc - Copy"
output_folder = "data/Goc-Enhance"

# Gọi hàm xử lý
process_images_in_folder(input_folder, output_folder)
