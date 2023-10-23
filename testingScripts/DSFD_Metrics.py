import csv

with open('testingDatas\\train\\train.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

with open('dsfd_output.csv', newline='') as f:
    reader = csv.reader(f)
    results = list(reader)

data_vals = [int(l[1]) for l in data]
results_vals = [int(l[1]) for l in results]

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


accuracy = accuracy_score(data_vals, results_vals)
precision = precision_score(data_vals, results_vals, average='micro')
recall = recall_score(data_vals, results_vals, average='micro')
f1 = f1_score(data_vals, results_vals, average='micro')
confusion = confusion_matrix(data_vals, results_vals)

print("accuracy", accuracy)
print("precision", precision)
print("recall", recall)
print("f1", f1)
print("confusion", confusion)

