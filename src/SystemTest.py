import joblib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score, \
    roc_curve
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine

classifier = joblib.load('../models/model_RF.pkl')

db_host = 'localhost'
db_port = '3306'
db_name = 'final_project'
db_url = f'mysql+pymysql://{db_host}:{db_port}/{db_name}'
engine = create_engine(db_url)
query = 'SELECT * FROM keystroke'
query2 = 'SELECT * FROM testset'
df = pd.read_sql(query, engine)
df_datapoint = pd.read_sql(query2, engine)
engine.dispose()

df = df.fillna(0)
z_scores = np.abs(stats.zscore(df.loc[:, 'key_1':'key_49'], axis=0))

threshold = 4
outlier_indices = np.where(z_scores > threshold)
df_cleaned = df.drop(outlier_indices[0])
y = df_cleaned['Target'].values
z = df_datapoint['Target'].values

scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_cleaned.loc[:, 'key_1':'key_49'])
new_data_point_scaled = scaler.transform(df_datapoint.loc[:, 'key_1':'key_49'])

estimator = LogisticRegression()
selector = RFE(estimator, n_features_to_select=5)
selector.fit_transform(df_scaled, y)
new_data_point_selected = selector.transform(new_data_point_scaled)

result = classifier.predict(new_data_point_selected)
print("Testing Set: ",z)
print("Prediction: ",result)

cm = confusion_matrix(z, result)
accuracy = accuracy_score(z, result)
precision = precision_score(z, result)
recall = recall_score(z, result)
f1 = f1_score(z, result)
auc_roc = roc_auc_score(z, result)

print(cm)
print("Accuracy:", accuracy)
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")
print(f"AUC_ROC: {auc_roc:.4f}")

fpr, tpr, thresholds = roc_curve(z, result)
plt.plot(fpr, tpr, label=f"AUC = {auc_roc:.2f}",)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
#plt.show()
print(thresholds)


