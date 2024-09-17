import numpy as np
from PIL import Image
import cv2


def load_binary_image(image_path):
    # Đọc ảnh và chuyển đổi thành ảnh nhị phân
    img = Image.open(image_path).convert('L')
    img_array = np.array(img)
    binary_array = (img_array > 246).astype(int)  # Ngưỡng 246 để chuyển thành nhị phân
    return binary_array


def save_subarray(binary_array, x, y, width, height):
    # Lấy mảng con tương ứng với vị trí và kích thước khung trượt
    return binary_array[y:y + height, x:x + width]


def sliding_window_and_save_arrays(image_path, window_width, window_height, step_size):
    # Load ảnh nhị phân
    binary_image = load_binary_image(image_path)
    img_height, img_width = binary_image.shape

    # Danh sách lưu các mảng con của khung trượt
    subarrays = []

    # Trượt khung hình chữ nhật trên ảnh
    for y in range(0, img_height - window_height + 1, step_size):
        for x in range(0, img_width - window_width + 1, step_size):
            # Lấy mảng con tương ứng với khung trượt
            subarray = save_subarray(binary_image, x, y, window_width, window_height)
            subarrays.append((subarray, x, y))  # Lưu cả vị trí của khung trượt

    return subarrays


def load_train_image(train_image_path):
    # Đọc ảnh train.jpg và chuyển đổi thành mảng nhị phân
    arr_train = load_binary_image(train_image_path)
    return arr_train


def compare_arrays(arr1, arr2):
    # So sánh hai mảng và đếm số điểm ảnh khác nhau
    if arr1.shape != arr2.shape:
        print("Hai mảng có kích thước khác nhau, không thể so sánh!")
        return None

    # So sánh và đếm số điểm khác nhau
    difference = np.sum(arr1 != arr2)
    return difference


def draw_rectangle_and_show(image_path, x, y, width, height):
    # Đọc ảnh gốc
    img = cv2.imread(image_path)

    # Vẽ hình chữ nhật trên ảnh
    cv2.rectangle(img, (x, y), (x + width, y + height), (0, 255, 0), 2)  # Màu xanh lá cây, độ dày 2

    # Hiển thị ảnh với hình chữ nhật
    cv2.imshow('Image with Rectangle', img)
    cv2.waitKey(0)  # Chờ người dùng nhấn phím để đóng cửa sổ
    cv2.destroyAllWindows()


# Sử dụng hàm
image_path = 'data/test/binary_test.jpg'  # Thay đường dẫn đến ảnh test của bạn
train_image_path = 'data/train/binary_22.jpg'  # Thay đường dẫn đến ảnh train.jpg của bạn
window_width = 50  # Chiều rộng khung hình chữ nhật
window_height = 540  # Chiều cao khung hình chữ nhật
step_size = 20  # Kích thước bước trượt (bạn có thể thay đổi giá trị này)

# Lấy các mảng nhị phân từ khung trượt của ảnh test.jpg
subarrays = sliding_window_and_save_arrays(image_path, window_width, window_height, step_size)

# Lưu ảnh nhị phân train.jpg vào mảng arr_train
arr_train = load_train_image(train_image_path)

# Tìm khung trượt có sự khác biệt nhỏ nhất
min_difference = float('inf')  # Khởi tạo giá trị khác biệt nhỏ nhất là vô cùng lớn
min_index = -1  # Chỉ số của mảng với khác biệt nhỏ nhất
min_x, min_y = 0, 0  # Vị trí của khung trượt có sự khác biệt nhỏ nhất

for i, (subarray, x, y) in enumerate(subarrays, start=1):
    difference = compare_arrays(subarray, arr_train)
    if difference is not None:
        if difference < min_difference:
            min_difference = difference
            min_index = i
            min_x, min_y = x, y

# In số điểm ảnh khác biệt nhỏ nhất và vẽ hình chữ nhật quanh khung trượt
if min_index != -1:
    print(f"Số điểm ảnh khác biệt nhỏ nhất là {min_difference} tại khung ảnh thứ {min_index}.")
    print(f"Vị trí của khung trượt là: ({min_x}, {min_y})")

    # Vẽ hình chữ nhật và hiển thị ảnh
    draw_rectangle_and_show('data/raw/test.jpg', min_x, min_y, window_width, window_height)
