from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np

n = KNeighborsClassifier(n_neighbors = 3)

#First, import the data from the test file (will be using example data)
#Will be replaced by HTTP requests in future iterations
data = pd.read_csv('Datasets\IRIS.csv')

output = data['species']
inputs = data.loc[:,~data.columns.isin(['species'])]

n.fit(inputs,output)

inputData = pd.read_csv('Datasets\IRIStest.csv')

outputCheck = inputData['species']
cleanInput = inputData.loc[:,~data.columns.isin(['species'])]

prediction = n.predict(cleanInput)


correct = 0
idx = 0
for i in outputCheck:
    if i == prediction[idx]:
        correct+=1
    idx+=1

print('Percentage correct predictions: ' + str(correct*100//idx) + '%')
