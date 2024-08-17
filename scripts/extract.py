import boto3
import os
from datetime import datetime, timedelta
from botocore.exceptions import NoCredentialsError, ClientError


# Get today's date
today = datetime.now()
yesterday = today - timedelta(days=1)
yesterday_str = yesterday.strftime('%Y%m%d')

print(yesterday_str)

# Configuration
s3_bucket_name = 'your-bucket-name'
file_name = f'mall_customers_{yesterday_str}.parquet'
local_download_path = 'intermediate_files/mall_customers_{yesterday_str}.parquet' 

# Create local directory if it doesn't exist
os.makedirs(local_download_path, exist_ok=True)

# Initialize S3 client
s3_client = boto3.client('s3')

# Alternate s3 client init
# s3 = boto3.client(
#     's3',
#     aws_access_key_id=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     aws_session_token=aws_session_token  # Optional
# )

try:
    s3_client.download_file(s3_bucket_name, file_name, local_download_path)
    print(f'Successfully downloaded {file_name} from bucket {s3_bucket_name} to {local_download_path}')
    
except NoCredentialsError:
    # Handle the case where AWS credentials are not provided
    print('Error: No AWS credentials found. Please configure your credentials.')

except ClientError as e:
    # Handle other client-side errors (e.g., bucket not found, file not found)
    error_code = e.response['Error']['Code']
    if error_code == '404':
        print(f'Error: The object {file_name} does not exist in the bucket {local_download_path}.')
        
    else:
        print(f'Client error occurred: {e}')

except Exception as e:
    # Handle any other exceptions
    print(f'An unexpected error occurred: {e}')


