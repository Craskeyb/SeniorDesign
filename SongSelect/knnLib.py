from sklearn.neighbors import KNeighborsClassifier

#Inputs = emotion, people count, motion, audio level, light intensisty, temp

x = []
y = []

n = KNeighborsClassifier(n_neighbors = 3)
