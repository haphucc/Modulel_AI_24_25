from PIL import Image
import os
from pathlib import Path


def resize_image(img, target_size=(128, 128)):
    """Hàm resize một ảnh"""
    # Lấy kích thước gốc
    width, height = img.size

    # Tính toán tỷ lệ để giữ aspect ratio
    aspect_ratio = width / height

    if aspect_ratio > 1:
        # Ảnh rộng hơn cao
        new_width = target_size[0]
        new_height = int(new_width / aspect_ratio)
    else:
        # Ảnh cao hơn rộng
        new_height = target_size[1]
        new_width = int(new_height * aspect_ratio)

    # Resize ảnh giữ tỷ lệ
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Tạo ảnh mới với kích thước target và nền đen
    new_img = Image.new('RGB', target_size, 'white')

    # Tính toán vị trí để paste ảnh vào giữa
    paste_x = (target_size[0] - new_width) // 2
    paste_y = (target_size[1] - new_height) // 2

    # Chuyển đổi sang chế độ RGBA để xử lý alpha channel
    if img_resized.mode != 'RGBA':
        img_resized = img_resized.convert('RGBA')

    # Paste ảnh đã resize vào ảnh mới
    new_img.paste(img_resized, (paste_x, paste_y), img_resized)

    return new_img


def process_folder(input_folder, output_folder, target_size=(128, 128)):
    """Hàm xử lý cả folder ảnh"""
    # Tạo thư mục output nếu chưa tồn tại
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Các định dạng ảnh được hỗ trợ
    supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}

    # Đếm số ảnh đã xử lý
    processed = 0
    errors = 0

    # Lặp qua tất cả các file trong thư mục input
    for filename in os.listdir(input_folder):
        # Lấy phần mở rộng của file
        file_ext = os.path.splitext(filename)[1].lower()

        # Kiểm tra nếu là file ảnh
        if file_ext in supported_formats:
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            try:
                # Mở và xử lý ảnh
                with Image.open(input_path) as img:
                    # Resize ảnh
                    new_img = resize_image(img, target_size)
                    # Lưu ảnh đã xử lý
                    new_img.save(output_path, quality=95)
                processed += 1
                print(f"Đã xử lý: {filename}")

            except Exception as e:
                print(f"Lỗi khi xử lý {filename}: {str(e)}")
                errors += 1

    # In thông kê kết quả
    print(f"\nKết quả xử lý:")
    print(f"- Tổng số ảnh đã xử lý thành công: {processed}")
    print(f"- Số ảnh bị lỗi: {errors}")
    print(f"- Thư mục output: {output_folder}")


# Sử dụng chương trình
input_folder = "data/Gray - Copy/new"  # Thay đổi thành đường dẫn thư mục chứa ảnh gốc
output_folder = "data/Gray-Resized"  # Thay đổi thành đường dẫn thư mục sẽ chứa ảnh đã xử lý

# Chạy xử lý
process_folder(input_folder, output_folder)
