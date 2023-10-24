import requests
import pandas as pd

url = "https://api.tgju.org/v1/market/indicator/summary-table-data/price_dollar_rl?lang=fa&order_dir=asc&draw=1&columns%255B0%255D%255Bdata%255D=0&columns%255B0%255D%255Bname%255D=&columns%255B0%255D%255Bsearchable%255D=true&columns%255B0%255D%255Borderable%255D=true&columns%255B0%255D%255Bsearch%255D%255Bvalue%255D=&columns%255B0%255D%255Bsearch%255D%255Bregex%255D=false&columns%255B1%255D%255Bdata%255D=1&columns%255B1%255D%255Bname%255D=&columns%255B1%255D%255Bsearchable%255D=true&columns%255B1%255D%255Borderable%255D=true&columns%255B1%255D%255Bsearch%255D%255Bvalue%255D=&columns%255B1%255D%255Bsearch%255"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data["data"])
    df = df.drop(columns=[0, 1, 2, 4, 5])
    df.rename(columns={3: "close_price", 6: "miladi", 7: "shamsi"}, inplace=True)
    df["close_price"] = df["close_price"].str.replace(",", "").astype(int)
    df["close_price"] = df["close_price"] / 10
    df["close_price"] = df["close_price"].astype(int)
    df.to_csv("dollar_price.csv")
else:
    print("Failed to retrieve data from the API.")