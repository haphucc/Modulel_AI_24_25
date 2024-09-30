'''
 chiều dài, chiều rộng của đài hoa
 chiều dài, chiều rộng của cánh hoa
 cột class

 Mau test
     1   5.1,3.5,1.4,0.2, Iris-setosa
     51  7.0,3.2,4.7,1.4, Iris-versicolor
     101 6.3,3.3,6.0,2.5, Iris-virginica
 Mau train
     iris-147.data
'''
import pandas as pd
import numpy as np

# Định nghĩa các cột cho tập dữ liệu Iris
columns = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)', 'Class']

# Đọc file CSV và gán tên cột
data_iris = pd.read_csv("iris-147.data", header=None, names=columns)

# Tạo bản sao của DataFrame
data_iris = data_iris.copy()

# Nhập vector test từ người dùng
k_value = int(input("Nhập giá trị K: "))
test_vector = np.array(list(map(float, input("Nhập vector test gồm 4 đặc trưng: ").split(','))))

# Hàm tính khoảng cách Manhattan
def manhattan_distance(row):
    return np.sum(np.abs(test_vector - row.iloc[:4]))

# Hàm tính khoảng cách Euclidean
def euclidean_distance(row):
    return round(np.sqrt(np.sum(np.square(test_vector - row.iloc[:4]))), 3)

# Tính khoảng cách Manhattan cho từng mẫu và thêm vào cột 'Manhattan_Distance'
data_iris['Manhattan_Distance'] = data_iris.apply(manhattan_distance, axis=1)

# Tính khoảng cách Euclidean cho từng mẫu và thêm vào cột 'Euclidean_Distance'
data_iris['Euclidean_Distance'] = data_iris.apply(euclidean_distance, axis=1)

# Sắp xếp theo khoảng cách Manhattan và lấy K hàng đầu tiên
nearest_manhattan = data_iris.nsmallest(k_value, 'Manhattan_Distance')

# Sắp xếp theo khoảng cách Euclidean và lấy K hàng đầu tiên
nearest_euclidean = data_iris.nsmallest(k_value, 'Euclidean_Distance')

print(f"\n{k_value} mẫu có khoảng cách Manhattan nhỏ nhất:")
print(nearest_manhattan[['Class', 'Manhattan_Distance']])

print(f"\n{k_value} mẫu có khoảng cách Euclidean nhỏ nhất:")
print(nearest_euclidean[['Class', 'Euclidean_Distance']])
