import numpy as np
from PIL import Image


def load_binary_image(image_path):
    img = Image.open(image_path).convert('L')
    img_array = np.array(img)
    binary_array = (img_array > 246).astype(int)
    return binary_array


def save_binary_array_to_txt(binary_array, output_txt_path):
    # Chuyển đổi mảng thành chuỗi
    binary_string = '\n'.join([''.join(map(str, row)) for row in binary_array])

    # Lưu chuỗi nhị phân vào file .txt
    with open(output_txt_path, 'w') as file:
        file.write(binary_string)
    print(f"Mảng nhị phân đã được lưu vào file '{output_txt_path}'")


def compare_and_save_binary_images(image1_path, image2_path, output_txt1, output_txt2):
    # Load hai ảnh nhị phân
    binary_image1 = load_binary_image(image1_path)
    binary_image2 = load_binary_image(image2_path)

    # Lưu từng mảng nhị phân vào file .txt
    save_binary_array_to_txt(binary_image1, output_txt1)
    save_binary_array_to_txt(binary_image2, output_txt2)

    # So sánh hai mảng
    difference = np.sum(binary_image1 != binary_image2)

    # Trả về số lượng điểm ảnh khác nhau
    print(f"Số lượng điểm ảnh khác nhau: {difference}")


# Sử dụng hàm
image1_path = 'data/train/binary_22.jpg'  # Thay đổi đường dẫn này
image2_path = 'data/train/binary_11.jpg'  # Thay đổi đường dẫn này
output_txt1 = 'data/output1.txt'  # Đường dẫn file .txt lưu ảnh 1
output_txt2 = 'data/output2.txt'  # Đường dẫn file .txt lưu ảnh 2

compare_and_save_binary_images(image1_path, image2_path, output_txt1, output_txt2)
