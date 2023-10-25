import requests
import pandas as pd


def create_df(data):
    df = pd.DataFrame(data["data"])
    df = df.drop(columns=[0, 1, 2, 4, 5])
    df.rename(columns={3: "close_price", 6: "miladi", 7: "shamsi"}, inplace=True)
    df["close_price"] = df["close_price"].str.replace(",", "").astype(int)
    df["close_price"] = df["close_price"] / 10
    df["close_price"] = df["close_price"].astype(int)

    df["miladi"] = pd.to_datetime(df["miladi"])
    start_date = df["miladi"].min()
    end_date = df["miladi"].max()

    date_range = pd.date_range(start=start_date, end=end_date, freq="D")
    missing_dates = date_range.difference(df["miladi"])
    missing_data = {"miladi": missing_dates, "close_price": None}
    missing_df = pd.DataFrame(missing_data)

    for index, row in missing_df.iterrows():
        closest_date = df["miladi"][df["miladi"] <= row["miladi"]].max()
        closest_price = df.loc[df["miladi"] == closest_date, "close_price"].values[0]
        missing_df.at[index, "close_price"] = closest_price

    df = pd.concat([df, missing_df], ignore_index=True)
    return df.sort_values(by="miladi").reset_index(drop=True)


url = "https://api.tgju.org/v1/market/indicator/summary-table-data/price_dollar_rl?lang=fa&order_dir=asc&draw=1&columns%255B0%255D%255Bdata%255D=0&columns%255B0%255D%255Bname%255D=&columns%255B0%255D%255Bsearchable%255D=true&columns%255B0%255D%255Borderable%255D=true&columns%255B0%255D%255Bsearch%255D%255Bvalue%255D=&columns%255B0%255D%255Bsearch%255D%255Bregex%255D=false&columns%255B1%255D%255Bdata%255D=1&columns%255B1%255D%255Bname%255D=&columns%255B1%255D%255Bsearchable%255D=true&columns%255B1%255D%255Borderable%255D=true&columns%255B1%255D%255Bsearch%255D%255Bvalue%255D=&columns%255B1%255D%255Bsearch%255"
response = requests.get(url)

if response.status_code == 200:
    df = create_df(response.json())
    df.to_csv("dollar_price.csv")
else:
    print("Failed to retrieve data from the API.")