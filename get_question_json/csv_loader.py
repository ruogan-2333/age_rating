import csv
from pprint import pprint
import pandas as pd  # 强烈推荐安装 pandas，后面会用

df = pd.read_csv('violence_mapping.csv')

columns = df.columns.tolist()
print(columns)
unique_values = df["violence_content"].dropna().unique().tolist()
print(unique_values)
# for column in columns:
#     unique_values = df[column].unique()
#     print(unique_values)
