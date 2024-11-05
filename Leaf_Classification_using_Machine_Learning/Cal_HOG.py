from skimage.io import imread
from skimage.feature import hog
from skimage.color import rgb2gray
import pandas as pd
import os
import csv

def get_label(filename):
    # Lấy số từ tên file (vd: img (66).jpg -> 66)
    number = int(filename.split('(')[-1].split(')')[0].strip())

    # Gán nhãn dựa trên số
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
    else:
        return 'Unknown'  # Nếu số không nằm trong khoảng đã định

def compute_hog_features(img_path):
    # Tính toán HOG features cho một ảnh
    img = imread(img_path)
    if len(img.shape) == 3:
        img = rgb2gray(img)
    features, _ = hog(img,
                      orientations=9,
                      pixels_per_cell=(8, 8),
                      cells_per_block=(2, 2),
                      visualize=True)
    return features

def process_image_directory(input_dir, output_csv):
    # Lấy danh sách tất cả các file ảnh và sắp xếp theo thứ tự số trong tên file
    image_files = sorted(
        [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))],
        key=lambda x: int(os.path.splitext(x)[0].split('_')[0])
                      if '_' in x else int(os.path.splitext(x)[0].split('(')[-1].split(')')[0])
    )

    # Khởi tạo list để lưu dữ liệu
    all_features = []
    image_paths = []

    print(f"Processing {len(image_files)} images...")
    for img_file in image_files:
        img_path = os.path.join(input_dir, img_file)
        try:
            features = compute_hog_features(img_path)
            all_features.append(features)
            image_paths.append(img_file)
            print(f"Đã xử lý: {img_file}")

        except Exception as e:
            print(f"Error processing {img_file}: {str(e)}")

    # Tạo DataFrame và thêm cột "Labels"
    feature_columns = [f'Feature HOG {i + 1}' for i in range(len(all_features[0]))]
    df = pd.DataFrame(all_features, columns=feature_columns)
    df.insert(0, 'Filename', image_paths)

    # Thêm cột Labels
    df['Labels'] = df['Filename'].apply(get_label)

    # Ghi header cho file CSV
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ['Filename'] + feature_columns + ['Labels']
        writer.writerow(header)

        # Ghi dữ liệu vào file CSV
        for index, row in df.iterrows():
            writer.writerow(row)

    print(f"\nSaved features for {len(image_paths)} images to: {output_csv}")
    print(f"Feature vector size: {len(feature_columns)}")

# Sử dụng function
input_directory = "data/Gray-Resized"  # Thay đổi đường dẫn theo thư mục của bạn
output_csv_file = "output_csv/feature_hog1.csv"  # Bạn có thể đổi tên file này
process_image_directory(input_directory, output_csv_file)
