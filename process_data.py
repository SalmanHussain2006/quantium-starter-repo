import pandas as pd

# Load the datasets
df1 = pd.read_csv('data/daily_sales_data_0.csv')
df2 = pd.read_csv('data/daily_sales_data_1.csv')
df3 = pd.read_csv('data/daily_sales_data_2.csv')

# Combine all datasets
df = pd.concat([df1, df2, df3], ignore_index=True)

# Filter only Pink Morsels
df = df[df['product'] == 'pink morsel']

# Clean the price column (remove $ and convert to float)
df['price'] = df['price'].replace({'\$': '', ',': ''}, regex=True).astype(float)

# Create Sales column
df['sales'] = df['quantity'] * df['price']

# Keep only required columns
output = df[['sales', 'date', 'region']]

# Rename columns
output = output.rename(columns={
    'sales': 'Sales',
    'date': 'Date',
    'region': 'Region'
})

# Save to CSV
output.to_csv('output.csv', index=False)

print("Processing complete. Output saved as output.csv")