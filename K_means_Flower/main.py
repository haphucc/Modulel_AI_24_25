import cv2
import numpy as np
from sklearn.cluster import KMeans


def extract_yellow_rose(image_path, k=3, max_iter=300):
    # Đọc ảnh
    image = cv2.imread(image_path)

    # Chuyển đổi ảnh sang không gian màu RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Reshape ảnh thành mảng 2D các pixel
    pixel_values = image_rgb.reshape((-1, 3))

    # Chuyển đổi sang kiểu float
    pixel_values = np.float32(pixel_values)

    # Áp dụng K-means
    kmeans = KMeans(n_clusters=k, max_iter=max_iter, n_init=10, random_state=42)
    kmeans.fit(pixel_values)

    # Lấy số vòng lặp thực tế
    n_iterations = kmeans.n_iter_

    # Lấy các tâm cụm
    centers = kmeans.cluster_centers_

    # Tìm cụm có màu gần với màu vàng nhất
    yellow_target = np.array([255, 255, 0])  # Màu vàng trong RGB
    distances = np.linalg.norm(centers - yellow_target, axis=1)
    yellow_cluster = np.argmin(distances)

    # Tạo mask cho hoa màu vàng
    labels = kmeans.labels_
    yellow_mask = np.where(labels == yellow_cluster, 255, 0).astype(np.uint8)
    yellow_mask = yellow_mask.reshape(image_rgb.shape[:2])

    # Tạo ảnh kết quả với hoa màu vàng trên nền đen
    result = np.zeros_like(image_rgb)
    result[yellow_mask == 255] = image_rgb[yellow_mask == 255]

    # Chuyển đổi kết quả sang BGR để hiển thị và lưu
    result_bgr = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)

    print(f"K-means đã chạy {n_iterations} vòng lặp.")

    return result_bgr, n_iterations


# Nhập số vòng lặp tối đa từ bàn phím
while True:
    try:
        max_iterations = int(input("Nhập số vòng lặp tối đa cho K-means (ít nhất 1): "))
        if max_iterations < 1:
            print("Số vòng lặp phải là số nguyên dương. Vui lòng nhập lại.")
        else:
            break
    except ValueError:
        print("Vui lòng nhập một số nguyên hợp lệ.")

# Sử dụng hàm
input_image_path = 'yellow.jpg'
output_image, iterations = extract_yellow_rose(input_image_path, max_iter=max_iterations)

print(f"Tổng số vòng lặp thực tế: {iterations}")

# Hiển thị kết quả
cv2.imshow('Extracted Yellow Rose', output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Lưu kết quả
cv2.imwrite('extracted_yellow_rose.jpg', output_image)