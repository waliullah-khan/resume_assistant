from astrapy import DataAPIClient
from dotenv import load_dotenv
import pandas as pd 
import os
from datetime import datetime
import numpy as np
from datasets import load_dataset
print("imports complete")
load_dotenv()
print("dotenv complete")
dataset = load_dataset("datastax/linkedin_job_listings", split='train')
print("dataset complete")
job_listings = pd.DataFrame.from_dict(dataset)
job_listings = job_listings.replace([np.nan, np.inf, -np.inf], None)
print("job_listings complete")

client = DataAPIClient(os.environ["ASTRA_DB_APPLICATION_TOKEN"])
print("client complete")
database = client.get_database(os.environ["ASTRA_DB_API_ENDPOINT"])
print("database complete")
collection = database.get_collection("job_listings")
print("collection complete")

def truncate_content(content, max_bytes=8000):
    # Encode the string into bytes (UTF-8 encoding)
    content_bytes = content.encode('utf-8')
    
    # Check if the byte length exceeds the limit
    if len(content_bytes) > max_bytes:
        # Truncate the content to the maximum byte size
        truncated_content_bytes = content_bytes[:max_bytes]
        
        # Decode back to a string, ensuring no decoding errors occur
        truncated_content = truncated_content_bytes.decode('utf-8', errors='ignore')
    else:
        truncated_content = content

    return truncated_content


import time

for index, row in job_listings.iterrows():
    print(row['title'])

    content = (row['title'] + "\n\n" + row['description'])
    counter = 0
    while True:
        try:
            print("counter", counter)
            collection.update_one(
                {'_id': row['job_id']},
                {'$set': {
                    'job_title': row['title'],
                    'company': row['company_name'],
                    '$vectorize': content,
                    'max_salary': row['max_salary'],
                    'pay_period': row['pay_period'],
                    'location': row['location'],
                    'job_url': row['job_posting_url'],
                    'content': truncate_content(content),
                    'metadata': {'ingested': datetime.now()}
                }},
                upsert=True
            )
            counter += 1
            break  # Exit the loop on success
        except Exception as ex:
            print(ex)
            print("Retrying...")
            time.sleep(5)  # Wait 5 seconds before retrying


