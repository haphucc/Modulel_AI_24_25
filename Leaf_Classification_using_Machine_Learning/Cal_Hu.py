import os
import numpy as np
import csv
from PIL import Image

# Hàm tính moments trung tâm
def central_moment(data, p, q, x_centroid, y_centroid):
    y, x = np.ogrid[:data.shape[0], :data.shape[1]]
    return np.sum(((x - x_centroid) ** p) * ((y - y_centroid) ** q) * data)

# Hàm tính moments trung tâm chuẩn hóa
def central_normalized_moment(moments, p, q, m00):
    return moments[f'm_{p}{q}'] / (m00 ** (((p + q) / 2) + 1))

# Hàm tính Hu moments (thay thế cho OpenCV)
def calculate_hu_moments(M):
    S = {}
    S[1] = M['M_20'] + M['M_02']
    S[2] = (M['M_20'] - M['M_02']) ** 2 + 4 * (M['M_11'] ** 2)
    S[3] = (M['M_30'] - 3 * M['M_12']) ** 2 + (3 * M['M_21'] - M['M_03']) ** 2
    S[4] = (M['M_30'] + M['M_12']) ** 2 + (M['M_03'] + M['M_21']) ** 2
    S[5] = (M['M_30'] - 3 * M['M_12']) * (M['M_30'] + M['M_12']) * ((M['M_30'] + M['M_12']) ** 2 - 3 * (M['M_03'] + M['M_21']) ** 2) + \
           (3 * M['M_21'] - M['M_03']) * (M['M_03'] + M['M_21']) * (3 * (M['M_30'] + M['M_12']) ** 2 - (M['M_03'] + M['M_21']) ** 2)
    S[6] = (M['M_20'] - M['M_02']) * ((M['M_30'] + M['M_12']) ** 2 - (M['M_03'] + M['M_21']) ** 2) + 4 * M['M_11'] * (M['M_30'] + M['M_12']) * (M['M_03'] + M['M_21'])
    S[7] = (3 * M['M_21'] - M['M_03']) * (M['M_30'] + M['M_12']) * ((M['M_30'] + M['M_12']) ** 2 - 3 * (M['M_03'] + M['M_21']) ** 2) - \
           (M['M_30'] - 3 * M['M_12']) * (M['M_03'] + M['M_21']) * (3 * (M['M_30'] + M['M_12']) ** 2 - (M['M_03'] + M['M_21']) ** 2)
    return [S[i] for i in range(1, 8)]

# Hàm lấy nhãn dựa trên số trong tên file
def get_label(filename):
    number = int(filename.split('(')[-1].split(')')[0].strip())
    if 1 <= number <= 50:
        return 'A'
    elif 51 <= number <= 100:
        return 'B'
    elif 101 <= number <= 150:
        return 'C'
    elif 151 <= number <= 200:
        return 'D'
    elif 201 <= number <= 250:
        return 'E'
    return 'Unknown'

# Hàm xử lý ảnh và trả về Hu moments
def process_image(image_path):
    im = Image.open(image_path).convert("L")
    threshold = 128
    im_bin = im.point(lambda p: 255 if p > threshold else 0)
    data = np.array(im_bin)
    m00 = np.sum(data == 255) * 255

    # Tính centroid của ảnh
    height, width = data.shape
    x_centroid = np.sum(np.arange(width) * np.sum(data, axis=0)) / m00
    y_centroid = np.sum(np.arange(height) * np.sum(data, axis=1)) / m00

    # Tính moments trung tâm bậc 3
    moments = {}
    for p in range(4):
        for q in range(4):
            if p + q <= 3:
                moments[f'm_{p}{q}'] = central_moment(data, p, q, x_centroid, y_centroid)

    # Tính moments chuẩn hóa trung tâm
    normalized_moments = {}
    for p in range(4):
        for q in range(4):
            if 0 < p + q <= 3:
                normalized_moments[f'M_{p}{q}'] = central_normalized_moment(moments, p, q, m00)

    # Tính Hu moments
    hu_moments = calculate_hu_moments(normalized_moments)

    # Đưa Hu moments về thang logarit để dễ so sánh
    # hu_moments_log = [round(-np.sign(m) * np.log10(abs(m)), 5) if m != 0 else 0 for m in hu_moments]
    # return hu_moments_log
    hu_moments_nolog = [m for m in hu_moments]
    return hu_moments_nolog

# Hàm xử lý folder và lưu kết quả vào CSV
def process_directory(input_directory, output_csv):
    files = sorted([f for f in os.listdir(input_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))],
                   key=lambda x: int(x.split('(')[-1].split(')')[0]))

    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Filename', 'Hu Moment 1', 'Hu Moment 2', 'Hu Moment 3', 'Hu Moment 4', 'Hu Moment 5', 'Hu Moment 6', 'Hu Moment 7', 'Labels'])

        for filename in files:
            file_path = os.path.join(input_directory, filename)
            hu_moments = process_image(file_path)
            label = get_label(filename)
            writer.writerow([filename] + hu_moments + [label])
            print(f"Đã xử lý: {filename}")

# Sử dụng hàm
input_dir = 'data/Bin'
output_csv = 'output_csv/feature_hu_moments_nolog.csv'
process_directory(input_dir, output_csv)
