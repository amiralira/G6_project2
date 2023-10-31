import numpy as np
import pandas as pd

file_dir = "TEKNOLIFEdata.xlsx"
file_dir2 = "dollar_price.csv"
file_dir3 = "technolife_data.csv"

df = pd.read_excel(file_dir)
# condition = df["other.1"].str.match("نوع کاربری")
condition = ~df["other.7"].isna()
df.loc[condition, "Size":"other.7"] = df.loc[condition, "Size":"other.7"].shift(
    -1, axis=1
)


def persian_numbers(row, col_name):
    row[col_name] = (
        row[col_name]
        .replace("۰", "0")
        .replace("۱", "1")
        .replace("۲", "2")
        .replace("۳", "3")
        .replace("۴", "4")
        .replace("۵", "5")
        .replace("۶", "6")
        .replace("۷", "7")
        .replace("۸", "8")
    )
    return row


def replace_memory(text):
    text = text.replace("و", "+")
    text = text.replace("_x000D_\n", " ")
    text = text.replace("یک", "1")
    text = text.replace(" ترابایت", "TB")
    text = (
        text.replace(" گيگابايت", "GB")
        .replace(" گیگابایت", "GB")
        .replace(" گیگابات", "GB")
    )
    return text.strip()


def replace_gpu(text):
    text = text.replace("ظرفیت حافظه داخلی", "")
    text = text.replace("ظرفیت حافظه SSD", "")
    text = text.replace("اینتل", "intel")
    text = text.replace("_x000D_", "")
    text = text.upper()
    text = text.replace("NVIDA", "NVIDIA")
    text = text.replace("1 ترابایت", "nan")
    text = text.replace("4 ترابایت", "nan")
    text = text.replace("256 گیگابایت", "nan")
    return text.strip()


df["Ram"] = df["Ram"].str[:2].str.strip()
df = df.apply(lambda row: persian_numbers(row, "Ram"), axis=1)
df["Ram"] = pd.to_numeric(df["Ram"], errors="coerce").fillna(0).astype(int)

df["Size"] = df["Size"].str.split().str[0]
df = df.apply(lambda row: persian_numbers(row, "Size"), axis=1)
df["Size"] = pd.to_numeric(df["Size"], errors="coerce")

df["CPU"] = df["CPU"].str.replace("ظرفیت حافظه RAM", "").str.strip()
df["graphic card"] = df["graphic card"].astype(str).apply(replace_gpu)

df["Memory"] = df["Memory"].astype(str).apply(replace_memory)
df = df.apply(lambda row: persian_numbers(row, "Memory"), axis=1)

df = df.drop(columns=["other.1", "other.7"])
# df = df.dropna(subset=["Price main", "Price off", "Price"], how="all")
df = df.dropna(subset=["Name"], how="all")
df = df.apply(lambda row: persian_numbers(row, "Name"), axis=1)

df["Price main"].fillna(df["Price"], inplace=True)
df["Price off"].fillna(df["Price"], inplace=True)
df.drop(columns="Price", inplace=True)
df["Price main"] = df["Price main"].str.replace(",", "")
df["Price off"] = df["Price off"].str.replace(",", "")
df["Price main"] = df["Price main"].fillna(0).astype(int)
df["Price off"] = df["Price off"].fillna(0).astype(int)

df["Manufacturer"] = df["Name"].str.split().str[0].str.lower()
df = df[df["graphic card"] != "nan"]
df = df[df["Memory"] != "nan"]
df = df.dropna().reset_index(drop=True)

df.rename(
    columns={
        "graphic card": "GPU",
        "Price main": "basePrice",
        "Price off": "salePrice",
        "Ram": "RAM",
        "Memory": "Storage",
        "Size": "Screen_Size",
    },
    inplace=True,
)
# Name, RAM, Storage, CPU_Manufacturer
# CPU_Model, CPU_Freq, GPU_Manufacturer
# GPU_Model, Screen_Size, basePrice, salePrice, saleType, Dollar_Price
df = df[
    [
        "Manufacturer",
        "Name",
        "RAM",
        "Storage",
        "CPU",
        "GPU",
        "Screen_Size",
        "basePrice",
        "salePrice",
    ]
]

df_dollar_price = pd.read_csv(file_dir2, index_col=[0])
df["Dollar_Price"] = df_dollar_price["close_price"].iloc[-1]
df.to_csv(file_dir3)