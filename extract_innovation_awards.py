import pandas as pd
import json

# Read the Excel file
xl = pd.ExcelFile('assets/webpage/2025_AI_Hackathon_Open_Sharing.xlsx')
print("Available sheets:")
for sheet in xl.sheet_names:
    print(f"  - {sheet}")

# Read the first sheet (or all sheets)
df = pd.read_excel('assets/webpage/2025_AI_Hackathon_Open_Sharing.xlsx', sheet_name=0)
print("\nFirst few rows:")
print(df.head(20).to_string())
