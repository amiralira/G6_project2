import requests
import numpy as np
import pandas as pd
import re

file_dir = "lipak_data.csv"
file_dir2 = "dollar_price.csv"


def find_first_number(text):
    matches = re.findall(r"[-+]?\d*\.\d+|\d+", str(text))
    if matches:
        return float(matches[0])
    return None


def find_pattern(text):
    pattern = re.search(r"[a-zA-Z]+.*?-", text)
    if pattern:
        return pattern.group(0)[:-1]
    return None


products_url = "https://lipak.com/api/v2/product?catId=%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE&pageNumber=0&pageSize=510"
response = requests.get(products_url)

if response.status_code == 200:
    data = response.json()
    products = data["productPage"]["content"]
    df = pd.DataFrame(products)
else:
    print("Failed to retrieve data from the API.")

df = df.drop(columns=["colors", "image", "satisfactionRate", "lpId", "remain"])
# df = df[df["saleType"] != "STOP"]

product_detail_url = "https://lipak.com/api/v1/shop/product-detail/"
df_res = pd.DataFrame()
imp_props = [
    "پردازنده مرکزی",
    "پردازنده گرافیکی",
    "حافظه RAM",
    "حافظه داخلی",
    "صفحه نمایش",
]
for slug in df["slug"]:
    url = product_detail_url + slug
    my_dict = {"slug1": slug}
    my_dict = pd.DataFrame.from_dict([my_dict])
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        featureGroups = data["featureGroups"]
        dfs = []
        for i_item in featureGroups:
            featureList = i_item["featureList"]
            if featureList == [] or i_item["name"] not in imp_props:
                continue
            for item in featureList:
                item["value"] = item["value"][0] if item["value"] else None
            df_temp = pd.DataFrame(featureList)
            df_temp = pd.DataFrame(
                columns=np.array(df_temp["name"]),
                data=np.array(df_temp["value"]).reshape(1, -1),
            )
            dfs.append(df_temp)

        dfs = pd.concat(dfs, axis=1)
        dfs = pd.concat([dfs, my_dict], axis=1)
        df_res = pd.concat([df_res, dfs], axis=0)
    else:
        print("Failed to retrieve data from the API.")
        # break

df_res = df_res.drop(
    columns=[
        "تعداد هسته",
        "حافظه Cache",
        "حافظه اختصاصی پردازنده گرافیکی",
        "نوع حافظه RAM",
        "قابلیت ارتقاء رم",
        "صفحه نمایش مات",
        "فناوری",
        "نوع حافظه داخلی",
        "نوع صفحه نمایش",
        "صفحه نمایش لمسی",
        "دقت صفحه نمایش",
    ]
).reset_index(drop=True)

df_temp = df_res.copy()
df_temp["فرکانس پردازنده"] = df_temp["فرکانس پردازنده"].fillna(
    df_temp["محدوده سرعت پردازنده"]
)
df_temp["مدل پردازنده"] = (
    df_temp["سری پردازنده"] + " " + df_temp["مدل پردازنده"]
).str.strip()
df_temp.drop(["محدوده سرعت پردازنده", "سری پردازنده"], axis=1, inplace=True)
df_temp["ظرفیت حافظه RAM"] = df_temp["ظرفیت حافظه RAM"].apply(find_first_number)
df_temp["ظرفیت حافظه داخلی"] = (
    df_temp["ظرفیت حافظه داخلی"]
    .replace(["یک", "گیگابایت", "ترابایت", "SSD"], ["1", "GB", "TB", ""], regex=True)
    .str.strip()
)
df_temp["فرکانس پردازنده"] = df_temp["فرکانس پردازنده"].apply(find_first_number)
df_temp["اندازه صفحه نمایش"] = df_temp["اندازه صفحه نمایش"].apply(find_first_number)
df_temp["مدل پردازنده گرافیکی"] = df_temp["مدل پردازنده گرافیکی"].str.strip()

df_temp = pd.merge(
    df_temp,
    df,
    how="left",
    left_on="slug1",
    right_on="slug",
)
df_temp.drop(columns=["slug1", "slug"], inplace=True)

df_temp["title"] = df_temp["title"].apply(find_pattern)
# df_temp["Manufacturer"] = df_temp["title"].str.split().str[0]
# df_temp["title"] = df_temp["title"].str.split(n=1).str[1]

df_temp.rename(
    columns={
        "title": "Name",
        "فرکانس پردازنده": "CPU_Freq",
        "سازنده پردازنده": "CPU_Manufacturer",
        "مدل پردازنده": "CPU_Model",
        "مدل پردازنده گرافیکی": "GPU_Model",
        "سازنده پردازنده گرافیکی": "GPU_Manufacturer",
        "ظرفیت حافظه RAM": "RAM",
        "ظرفیت حافظه داخلی": "Storage",
        "اندازه صفحه نمایش": "Screen_Size",
    },
    inplace=True,
)
df_temp = df_temp[
    [
        # "Manufacturer",
        "Name",
        "RAM",
        "Storage",
        "CPU_Manufacturer",
        "CPU_Model",
        "CPU_Freq",
        "GPU_Manufacturer",
        "GPU_Model",
        "Screen_Size",
        "basePrice",
        "salePrice",
        "saleType",
    ]
]
df_temp = df_temp.dropna().reset_index(drop=True)
df_temp["RAM"] = df_temp["RAM"].astype(int)

df_dollar_price = pd.read_csv(file_dir2, index_col=[0])
df_temp['Dollar_Price'] = df_dollar_price['close_price'].iloc[-1]
df_temp.to_csv(file_dir)