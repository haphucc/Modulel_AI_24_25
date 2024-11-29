import os
import cv2
import numpy as np

# Đường dẫn đến thư mục chứa ảnh dâu sống và chín
raw_folder_path = r'E:\HK9\AI\Strawberry\Neg'  # Thư mục chứa ảnh dâu sống
ripe_folder_path = r'E:\HK9\AI\Strawberry\Pos'  # Thư mục chứa ảnh dâu chín

# Hàm tính tỷ lệ cường độ màu đỏ trên tổng cường độ của 3 kênh (R, G, B)
def calculate_red_ratio(window):
    window_rgb = cv2.cvtColor(window, cv2.COLOR_BGR2RGB)
    red = window_rgb[:, :, 0].astype(float)
    green = window_rgb[:, :, 1].astype(float)
    blue = window_rgb[:, :, 2].astype(float)
    total_intensity = red + green + blue
    total_intensity[total_intensity == 0] = 1  # Tránh chia cho 0
    red_ratio = red / total_intensity
    avg_red_ratio = np.mean(red_ratio)
    return avg_red_ratio

# Tính tỷ lệ đỏ cho tất cả các ảnh trong thư mục dâu sống
raw_ratios = []
for image_name in os.listdir(raw_folder_path):
    if image_name.endswith((".jpg", ".png", ".jpeg")):
        full_image_path = os.path.join(raw_folder_path, image_name)
        red_ratio = calculate_red_ratio(cv2.imread(full_image_path))
        if red_ratio is not None:
            raw_ratios.append(red_ratio)
# Tính tỷ lệ đỏ cho tất cả các ảnh trong thư mục dâu chín
ripe_ratios = []
for image_name in os.listdir(ripe_folder_path):
    if image_name.endswith((".jpg", ".png", ".jpeg")):
        full_image_path = os.path.join(ripe_folder_path, image_name)
        red_ratio = calculate_red_ratio(cv2.imread(full_image_path))
        if red_ratio is not None:
            ripe_ratios.append(red_ratio)

threshold = 0.4138
print(f"Ngưỡng phân loại dâu chín: {threshold:.4f}")

# Bước 2: Phát hiện quả dâu chín
input_image_path = r'E:\HK9\AI\Strawberry\Test2\test16.jpeg'
input_image = cv2.imread(input_image_path)

# Định nghĩa kích thước cửa sổ và bước nhảy
window_size = 700 # Kích thước cửa sổ vuông
step_size = window_size // 2  # Bước nhảy là một nửa chiều dài cạnh cửa sổ

# Hàm cửa sổ trượt để phát hiện đối tượng
def sliding_window(input_image, window_size, step_size):
    # Duyệt qua cửa sổ trong ảnh
    for y in range(0, input_image.shape[0] - window_size + 1, step_size):
        for x in range(0, input_image.shape[1] - window_size + 1, step_size):
            yield (x, y, input_image[y:y + window_size, x:x + window_size])

# Phát hiện quả dâu chín
for (x, y, window) in sliding_window(input_image, window_size, step_size):
    red_ratio = calculate_red_ratio(window)
    print(f"Vị trí ({x}, {y}) - Tỷ lệ đỏ: {red_ratio:.4f}")  # Hiển thị tỷ lệ đỏ tại mỗi vị trí
    if red_ratio > threshold:
        # Vẽ khung màu vàng quanh quả dâu chín được phát hiện
        cv2.rectangle(input_image, (x, y), (x + window_size, y + window_size), (0, 255, 255), 2)

# Hiển thị kết quả chỉ với những quả dâu chín
cv2.namedWindow("Detected Strawberries", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Detected Strawberries", 1920,1080) 
cv2.imshow("Detected Strawberries", input_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

