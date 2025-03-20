import pandas as pd
from sqlalchemy import create_engine

db_host = 'localhost'  # Often 'localhost'
db_port = '3306'  # Often 3306
db_name = 'final_project'

# Create a connection string
db_url = f'mysql+pymysql://{db_host}:{db_port}/{db_name}'

# Create a database engine
engine = create_engine(db_url)

# SQL query to retrieve data (replace with your own query)
query = 'SELECT * FROM keystroke'

# Load data into a pandas DataFrame
data_frame = pd.read_sql(query, engine)

# Close the database connection
engine.dispose()

# Display the loaded data
print(data_frame)
