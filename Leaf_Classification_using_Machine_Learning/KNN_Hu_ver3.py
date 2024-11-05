import pandas as pd
import numpy as np
from collections import Counter
from sklearn.model_selection import StratifiedKFold, KFold
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support, accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt

def knn_predict(train_data, test_vector, k_value):
    distances = train_data.apply(
        # lambda row: np.sum(np.abs(test_vector - row.iloc[:7])), axis=1)
        lambda row: np.sqrt(np.sum(np.square(test_vector - row.iloc[:7]))), axis=1)
    nearest_indices = distances.nsmallest(k_value).index
    nearest_labels = train_data.loc[nearest_indices, 'Labels']
    return Counter(nearest_labels).most_common(1)[0][0]

def plot_confusion_matrix(conf_matrix, fold_num):
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Ma trận nhầm lẫn - Fold {fold_num}')
    plt.ylabel('Nhãn thực tế')
    plt.xlabel('Nhãn dự đoán')
    plt.show()

def evaluate_fold(train_data, test_data, k_value):
    y_true = test_data['Labels'].values
    y_pred = []

    # Get predictions for each test sample
    for idx, row in test_data.iterrows():
        test_vector = row.iloc[:7].values
        prediction = knn_predict(train_data, test_vector, k_value)
        y_pred.append(prediction)

    # Print detailed comparison
    print("So sánh chi tiết dự đoán:")
    print("Ground Truth: ", end="")
    for true in y_true:
        print(f"{true:3}", end=" ")
    print("\nPredicted:    ", end="")
    for pred in y_pred:
        print(f"{pred:3}", end=" ")
    # print("\nIndex:        ", end="")
    # for i in range(len(y_true)):
    #     print(f"{i:3}", end=" ")
    # print("\n")

    # Calculate metrics
    conf_matrix = confusion_matrix(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted')
    acc = accuracy_score(y_true, y_pred)

    # Print summary statistics

    # print("\nThống kê tổng hợp:")
    counts = Counter(zip(y_true, y_pred))
    # print("\nChi tiết dự đoán theo lớp:")
    for (true, pred), count in sorted(counts.items()):
        print(f"Ground Truth: {true}, Predicted: {pred}, Count: {count}")
    '''
    # Calculate per-class accuracy
    classes = sorted(set(y_true))
    print("\nĐộ chính xác theo từng lớp:")
    for cls in classes:
        mask = (y_true == cls)
        class_acc = accuracy_score(y_true[mask], np.array(y_pred)[mask])
        print(f"Lớp {cls}: {class_acc:.4f}")
    '''
    return conf_matrix, precision, recall, f1, acc


# Update the main loop to use the modified evaluation
k_value = int(input("Nhập giá trị K cho K-NN: "))

# Đọc và chuẩn bị dữ liệu
data_leaf = pd.read_csv("output_csv/feature_hu_moments_nolog.csv")
hu_moments_columns = data_leaf.columns[1:8]
data_leaf = data_leaf[list(hu_moments_columns) + ['Labels']]

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
# skf = KFold(n_splits=5, shuffle=True, random_state=42)
all_metrics = []
total_conf_matrix = None
fold_num = 1

X = data_leaf[hu_moments_columns]
y = data_leaf['Labels']

for train_index, test_index in skf.split(X, y):
    train_data = data_leaf.iloc[train_index]
    test_data = data_leaf.iloc[test_index]

    print(f"\n{'=' * 50}")
    print(f"Fold {fold_num}")
    print(f"{'=' * 50}")

    # Evaluate fold with detailed predictions
    conf_matrix, precision, recall, f1, accuracy = evaluate_fold(train_data, test_data, k_value)

    if total_conf_matrix is None:
        total_conf_matrix = conf_matrix
    else:
        total_conf_matrix += conf_matrix

    all_metrics.append({
        'Fold': fold_num,
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1-score': f1
    })

    # print(f"\nKết quả tổng hợp Fold {fold_num}:")
    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-score: {f1:.4f}")
    print("\nConfusion Matrix:")
    print(conf_matrix)
    plot_confusion_matrix(conf_matrix, fold_num)
    fold_num += 1

print(f"{'=' * 50}")
# Hiển thị confusion matrix gộp
print("Confusion Matrix after 5 fold:")
print(total_conf_matrix)

plt.figure(figsize=(8, 6))
sns.heatmap(total_conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.title("Ma trận nhầm lẫn sau 5 Fold")
plt.ylabel('Nhãn thực tế')
plt.xlabel('Nhãn dự đoán')
plt.show()

# Tính toán và in metrics trung bình
metrics_df = pd.DataFrame(all_metrics)
# print("\nMetrics trung bình qua tất cả các fold:")
print(f"\n{metrics_df.mean()[1:].round(4)}")