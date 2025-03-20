import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine
from sklearn.feature_selection import RFE

pd.set_option('display.max_rows', None)

db_host = 'localhost'
db_port = '3306'
db_name = 'final_project'
db_url = f'mysql+pymysql://{db_host}:{db_port}/{db_name}'
engine = create_engine(db_url)
query = 'SELECT * FROM keystroke'
df = pd.read_sql(query, engine)
engine.dispose()

df = df.fillna(0)
z_scores = np.abs(stats.zscore(df.loc[:, 'key_1':'key_49'], axis=0))
threshold = 4
outlier_indices = np.where(z_scores > threshold)
df_cleaned = df.drop(outlier_indices[0])
y = df_cleaned['Target'].values

scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_cleaned.loc[:, 'key_1':'key_49'])

estimator = LogisticRegression()
selector = RFE(estimator, n_features_to_select=5)
df_new = selector.fit_transform(df_scaled, y)

X_train, X_test, y_train, y_test = train_test_split(df_new, y, test_size=0.2, random_state=42)






