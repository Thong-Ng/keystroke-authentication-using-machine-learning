import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine


def isolation_demo(key):
    db_host = 'localhost'
    db_port = '3306'
    db_name = 'final_project'
    db_url = f'mysql+pymysql://{db_host}:{db_port}/{db_name}'
    engine = create_engine(db_url)
    query = "SELECT * FROM keystroke"
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
    new_data_point_scaled = scaler.transform([key])  # Modify

    estimator = LogisticRegression()
    selector = RFE(estimator, n_features_to_select=5)
    df_new = selector.fit_transform(df_scaled, y)
    new_data_point_selected = selector.transform(new_data_point_scaled)

    isolation_forest = IsolationForest(contamination=0.2, random_state=42)
    isolation_forest.fit(df_new)

    ood_predictions = isolation_forest.predict(new_data_point_selected)
    return ood_predictions


"""
    if ood_predictions == 1:
        print("User login successfully")
    elif ood_predictions == -1:
        print("Only authorized user is allowed!")
    #query2 = 'SELECT * FROM mixset_demo where User_ID = "A1"' #Modify
    #df_datapoint = key #Modify
"""

if __name__ == "__main__":
    isolation_demo()
