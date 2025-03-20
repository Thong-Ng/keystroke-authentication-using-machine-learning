import joblib
from sklearn.neural_network import MLPClassifier
from DataPreprocess import X_train, y_train, X_test, y_test
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score, roc_auc_score

mlp_classifier = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=2000, random_state=42)
mlp_classifier.fit(X_train, y_train)

y_pred = mlp_classifier.predict(X_test)
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
joblib.dump(mlp_classifier, "../models/model_MLP.pkl")

