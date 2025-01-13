from datasets import load_dataset
import pandas as pd
ds = load_dataset("datastax/linkedin_job_listings")
df = pd.DataFrame(ds)

print (df.columns())