import joblib
from sklearn.svm import SVC
from DataPreprocess import X_train, y_train, X_test, y_test
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score, roc_auc_score

svm_classifier = SVC(kernel='linear', C=0.1)
svm_classifier.fit(X_train, y_train)

y_pred = svm_classifier.predict(X_test)
print("Testing Set: ",y_test)
print("Prediction: ",y_pred)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
auc_roc = roc_auc_score(y_test, y_pred)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 score:", f1)
print(f"AUC_ROC: {auc_roc:.4f}")
print(cm)
joblib.dump(svm_classifier, "../models/model_SVM.pkl")

