import joblib
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine


def random_forest_demo():
    classifier = joblib.load('../models/model_RF.pkl')

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

    key = df_cleaned.iloc[0, 4:53].values
    key_df = pd.DataFrame([key], columns=df_cleaned.loc[:, 'key_1':'key_49'].columns)
    new_data_point_scaled = scaler.transform(key_df)

    estimator = LogisticRegression()
    selector = RFE(estimator, n_features_to_select=5)
    selector.fit_transform(df_scaled, y)
    new_data_point_selected = selector.transform(new_data_point_scaled)

    result = classifier.predict(new_data_point_selected)
    return result


if __name__ == "__main__":
    random_forest_demo()
