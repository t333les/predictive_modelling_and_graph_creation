import pandas as pd
import matplotlib.pyplot as plt

# Load the preprocessed data
data = pd.read_csv('preprocessed_clinical_trials_data.csv')

# Convert the "Study First Post Date" column to a DatetimeIndex
data['Study First Post Date'] = pd.to_datetime(data['Study First Post Date'])

# Set the "Study First Post Date" column as the index
data.set_index('Study First Post Date', inplace=True)

# Group the data by year and count the number of studies in each year
yearly_counts = data.resample('Y').size()

# Plot the time series
plt.figure(figsize=(12, 6))
yearly_counts.plot(title='Number of AI Studies in Healthcare Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Studies')
plt.show()

