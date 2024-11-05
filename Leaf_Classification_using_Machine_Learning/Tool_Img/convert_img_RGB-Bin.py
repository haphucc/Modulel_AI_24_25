'''
bit 0 chỉ màu đen và bit 1 chỉ màu trắng
0 chỉ màu đen, và 255 chỉ màu trắng, và 127 chỉ màu xám
'''

import os
from PIL import Image

def convert_images(input_directory, output_directory, threshold=220):
    # Lấy tên thư mục từ đường dẫn input_directory
    folder_name = os.path.basename(input_directory)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Lặp qua tất cả các tệp trong thư mục đầu vào
    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_directory, filename)

            with Image.open(input_path) as img:
                # Chuyển đổi sang ảnh xám
                gray_img = img.convert('L')

                # Chuyển đổi sang ảnh nhị phân
                binary_img = gray_img.point(lambda x: 255 if x < threshold else 0, 'L')

                # Giữ nguyên tên file output_csv theo định dạng gốc "IMG (Số thứ tự).jpg"
                filename = filename.lower()
                output_path = os.path.join(output_directory, filename)

                # Lưu ảnh đã chuyển đổi
                binary_img.save(output_path)
                print(f"Đã chuyển đổi: {filename}")

# Sử dụng hàm
input_dir = "data/Goc_2"
output_dir = "data/Bin_2"
convert_images(input_dir, output_dir)
