'''
 chiều dài, chiều rộng của đài hoa
 chiều dài, chiều rộng của cánh hoa
 cột class

 Mau test
     1   5.1,3.5,1.4,0.2,Iris-setosa
     51  7.0,3.2,4.7,1.4,Iris-versicolor
     101 6.3,3.3,6.0,2.5,Iris-virginica
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
    # Bỏ qua cột 'Class'
    return np.sum(np.abs(test_vector - row[:-1]))

# Tính khoảng cách cho từng mẫu và thêm vào cột 'distance'
data_iris['Distance'] = data_iris.apply(manhattan_distance, axis=1)

# In khoảng cách từ vector test đến từng mẫu
# print("\nKhoảng cách từ vector test đến từng mẫu:")
# print(data_iris[['Class', 'Distance']])

# Sắp xếp theo khoảng cách và lấy K hàng đầu tiên (khoảng cách nhỏ nhất)
nearest_rows = data_iris.nsmallest(k_value, 'Distance')

print(f"\n{k_value} mẫu có khoảng cách nhỏ nhất:")
print(nearest_rows[['Class', 'Distance']])

# Nếu muốn in lớp và khoảng cách của mẫu gần nhất nhất
print(f"\nKết quả: Vector test thuộc class {nearest_rows.iloc[0]['Class']} với khoảng cách nhỏ nhất là {nearest_rows.iloc[0]['Distance']:.2f}")

