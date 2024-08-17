import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError


# Get today's date
today = datetime.now()
yesterday = today - timedelta(days=1)
yesterday_str = yesterday.strftime('%Y%m%d')

print(yesterday_str)

local_download_path = 'intermediate_files/mall_customers_{yesterday_str}.parquet'
df = pd.read_parquet(local_download_path)
source = "mall_customers_{yesterday_str}.parquet"
df["source"] = source

# Define your PostgreSQL connection parameters
DATABASE_URL = "postgresql+psycopg2://pguser:pgpswd@localhost:5432/mydatabase"

# Create a database engine
engine = create_engine(DATABASE_URL)

table_name = 'mall_customers'

delete_old_data_sql = text(f"DELETE FROM {table_name} WHERE source = '{source}';")

try: 
    with engine.connect() as connection:
        with connection.begin() as transaction:
            # Delete old data based on the 'source' column
            result = connection.execute(delete_old_data_sql)
            rows_affected = result.rowcount
            print(f"Number of rows deleted: {rows_affected}")
except SQLAlchemyError as e:
    print(f"An error occurred: {e}")

finally:
    print("Operation completed.")


# Upload DataFrame to PostgreSQL, appending data if the table exists
df.to_sql('mall_customers', engine, if_exists='append', index=False)