import pandas as pd
import json

# Read 2024 data
df_2024 = pd.read_excel('data/2024.xlsx')
slide_idx_2024 = df_2024[df_2024['Topic'] == 'Slide'].index[0]
summary_idx_2024 = df_2024[df_2024['Topic'] == 'One sentence summary of What, Why, Benefits & How '].index[0]

data_2024 = {}
for col in df_2024.columns[1:]:
    data_2024[col] = {
        'slide': str(df_2024.iloc[slide_idx_2024][col]) if pd.notna(df_2024.iloc[slide_idx_2024][col]) else '',
        'summary': str(df_2024.iloc[summary_idx_2024][col]) if pd.notna(df_2024.iloc[summary_idx_2024][col]) else ''
    }

# Read 2025 data
df_2025 = pd.read_excel('data/2025.xlsx')
slide_idx_2025 = df_2025[df_2025['Topic'] == 'Slide'].index[0]
summary_idx_2025 = df_2025[df_2025['Topic'] == 'One sentence summary of What, Why, Benefits & How '].index[0]

data_2025 = {}
for col in df_2025.columns[1:]:
    data_2025[col] = {
        'slide': str(df_2025.iloc[slide_idx_2025][col]) if pd.notna(df_2025.iloc[slide_idx_2025][col]) else '',
        'summary': str(df_2025.iloc[summary_idx_2025][col]) if pd.notna(df_2025.iloc[summary_idx_2025][col]) else ''
    }

print("2024 DATA:")
print(json.dumps(data_2024, indent=2))
print("\n2025 DATA:")
print(json.dumps(data_2025, indent=2))
