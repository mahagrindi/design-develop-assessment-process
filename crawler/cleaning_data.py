import pandas as pd

# Read the Excel file into a DataFrame
df = pd.read_excel("startup_data.xlsx")

# Filter out rows with "phone" or "email" equal to "n.a."
df_filtered = df[ (df['email'] != 'n.a.')]

# Create a DataFrame containing the removed rows
df_removed = df[ (df['email'] == 'n.a.')]

# Save the filtered DataFrame to a new Excel file
df_filtered.to_excel("output_file_filtered.xlsx", index=False)

# Save the removed DataFrame to another Excel file
df_removed.to_excel("output_file_removed.xlsx", index=False)
