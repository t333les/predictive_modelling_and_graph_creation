import pandas as pd
import re
import datetime

data = pd.read_csv('clinical_trials_data_final.csv')

print("Initial number of rows:", len(data))

# Convert date columns to datetime objects
data['Completion Date'] = pd.to_datetime(data['Completion Date'], infer_datetime_format=True, errors='coerce')
data['Study First Post Date'] = pd.to_datetime(data['Study First Post Date'], infer_datetime_format=True, errors='coerce')

# Handle missing 'Completion Date' values
missing_completion_date = data['Completion Date'].isnull().sum()
print(f"Number of rows with missing 'Completion Date': {missing_completion_date}")
data.dropna(subset=['Completion Date'], inplace=True)

# Save the cleaned data to a new CSV file
data.to_csv('cleaned_clinical_trials_data.csv', index=False)
