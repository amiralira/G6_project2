import numpy as np
import pandas as pd

file_dir = "sales_data.csv"
file_dir2 = "country-cities-data.csv"

df = pd.read_csv(file_dir, low_memory=False)

df_pupulation = pd.read_csv(file_dir2)
df_pupulation.loc[15, "city"] = "Hamedan"

df_branchs = pd.DataFrame(columns=["Branch", "Sum_Sell", "Total_Price", "Profit"])

for branch in df["Branch"].unique():
    temp = df[df["Branch"] == branch]
    df_branchs.loc[len(df_branchs.index) + 1] = {
        "Branch": branch,
        "Sum_Sell": len(temp),
        "Total_Price": temp["Total_Price"].sum(),
        "Profit": temp["Profit"].sum(),
    }

df_branchs["Profit_key"] = df_branchs["Profit"] / df_branchs["Total_Price"]

df_branchs = pd.merge(
    df_branchs,
    df_pupulation,
    how="left",
    left_on="Branch",
    right_on="city",
)
df_branchs = df_branchs.drop(columns=["city", "country", "latitude", "longitude"])

weight_profit = 0.4
weight_margin = 0.3
weight_sales = 0.2
weight_population = 0.1

df_branchs["Weighted_Score"] = (
    df_branchs["Profit"] * weight_profit
    + df_branchs["Profit_key"] * weight_margin
    + df_branchs["Sum_Sell"] * weight_sales
    + df_branchs["pop2023"] * weight_population
)

df_branchs = df_branchs.sort_values(by=["Weighted_Score"], ascending=False)