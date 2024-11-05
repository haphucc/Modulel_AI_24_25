import cv2
import os


def convert_images_to_grayscale(input_folder, output_folder):
    """
    Chuyển đổi tất cả ảnh trong thư mục đầu vào sang ảnh xám
    và lưu chúng vào thư mục đầu ra.

    Parameters:
    - input_folder: Đường dẫn đến thư mục chứa ảnh đầu vào.
    - output_folder: Đường dẫn đến thư mục để lưu ảnh đầu ra.
    """
    # Tạo thư mục đầu ra nếu chưa tồn tại
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Duyệt qua từng tệp trong thư mục đầu vào
    for filename in os.listdir(input_folder):
        # Kiểm tra nếu file là ảnh (có thể mở rộng thêm các định dạng khác nếu cần)
        if filename.endswith('.jpg') or filename.endswith('.png'):
            # Đọc ảnh từ đường dẫn đầu vào
            img = cv2.imread(os.path.join(input_folder, filename))

            # Kiểm tra nếu ảnh được đọc thành công
            if img is not None:
                # Chuyển ảnh sang grayscale
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Đường dẫn lưu ảnh đầu ra
                output_path = os.path.join(output_folder, filename)

                # Lưu ảnh grayscale vào thư mục đầu ra
                cv2.imwrite(output_path, gray_img)
                print(f'Đã lưu ảnh grayscale: {output_path}')
            else:
                print(f'Không thể đọc ảnh: {filename}')


# Sử dụng hàm với đường dẫn cụ thể
input_folder = "data/Goc - Copy/new"
output_folder = "data/Gray"
convert_images_to_grayscale(input_folder, output_folder)
