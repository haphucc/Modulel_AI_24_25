import math 
 
a = float(input("Nhập giá trị a: ")) 
b = float(input("Nhập giá trị b: ")) 
c = float(input("Nhập giá trị c: ")) 
 
delta = b**2 - 4*a*c 
 
if delta > 0:
   # Phương trình có 2 nghiệm phân biệt
   x1 = (-b + math.sqrt(delta)) / (2*a)
   x2 = (-b - math.sqrt(delta)) / (2*a)
   print(f"Phương trình có 2 nghiệm phân biệt: x1 = {x1}, x2 = {x2}")

elif delta == 0:
   # Phương trình có nghiệm kép
   x1 = x2 = -b / (2*a)
   print(f"Phương trình có nghiệm kép: x1 = x2 = {x1}")

else:
   # Phương trình vô nghiệm thực
   print("Phương trình vô nghiệm thực.")