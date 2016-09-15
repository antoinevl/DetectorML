from slearn import svm
X = [[3, 3], [4, 4]]
y = [0, 1]
clf = svm.SVC() # instantiation
clf.fit(X, y) # training
clf.predict([[2, 2]]) # prediction
