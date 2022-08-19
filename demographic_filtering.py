import pandas as pd
import numpy as np

df = pd.read_csv("articles.csv")
df_sorted = df.sort_values(["total_events"], ascending=[True])

output = df_sorted.head(20)