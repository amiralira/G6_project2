import numpy as np
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.engine import create_engine
from jdatetime import datetime


file_dir = "sales_data.csv"
file_dir2 = "dollar_price.csv"
# Enter the following values to connect to the database
user = ""
password = ""
host = "localhost"
port = 3306
database = "project2"


def connect_database(my_db, my_cursor, host, user, password, database_name):
    try:
        my_db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database_name,
        )
        my_cursor = my_db.cursor()
        return my_db, my_cursor
    except:
        print("Error in connect_database function")


def disconnect_database(my_db, my_cursor):
    try:
        my_cursor.close()
        my_db.close()
        return my_db, my_cursor
    except:
        print("Error in disconnect_database function")


my_db = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
)
my_cursor = my_db.cursor()
my_cursor.execute("CREATE DATABASE " + database)
my_db.commit()
my_db, my_cursor = disconnect_database(my_db, my_cursor)

create_manufacturers_table_query = """
CREATE TABLE Manufacturers (
    ID INT,
    Name VARCHAR(15),
    CONSTRAINT PK_Manufacturers PRIMARY KEY (ID)
)
"""

create_categories_table_query = """
CREATE TABLE Categories (
    ID INT,
    Name VARCHAR(31),
    CONSTRAINT PK_CPUs PRIMARY KEY (ID)
)
"""

create_CPUs_table_query = """
CREATE TABLE CPUs (
    ID INT,
    Model VARCHAR(31),
    Frequency FLOAT,
    Manufacturer_ID INT,
    CONSTRAINT PK_CPUs PRIMARY KEY (ID),
    CONSTRAINT FK_CPUs_Manufacturers FOREIGN KEY (Manufacturer_ID) REFERENCES Manufacturers(ID)
)
"""

create_GPUs_table_query = """
CREATE TABLE GPUs (
    ID INT,
    Model VARCHAR(31),
    Manufacturer_ID INT,
    CONSTRAINT PK_GPUs PRIMARY KEY (ID),
    CONSTRAINT FK_GPUs_Manufacturers FOREIGN KEY (Manufacturer_ID) REFERENCES Manufacturers(ID)
)
"""

create_storages_table_query = """ 
CREATE TABLE Storages (
    ID INT,
    Model VARCHAR(30),
    CONSTRAINT PK_Storages PRIMARY KEY (ID)
)
"""

create_RAMs_table_query = """
CREATE TABLE RAMs (
    ID INT,
    Size INT,
    CONSTRAINT PK_RAMs PRIMARY KEY (ID)
)
"""

create_screens_table_query = """
CREATE TABLE Screens (
    ID INT,
    Size FLOAT,
    Resolution VARCHAR(15),
    Type VARCHAR(63),
    CONSTRAINT PK_Screens PRIMARY KEY (ID)
)
"""

create_OSs_table_query = """
CREATE TABLE OSs (
    ID INT,
    Name VARCHAR(15),
    Version VARCHAR(7),
    CONSTRAINT PK_OSs PRIMARY KEY (ID)
)
"""

create_specs_table_query = """
CREATE TABLE Specs (
    ID INT,
    Weight FLOAT,
    CPU_ID INT,
    GPU_ID INT,
    Storage_ID INT,
    RAM_ID INT,
    Screen_ID INT,
    OS_ID INT,
    CONSTRAINT PK_Specs PRIMARY KEY (ID),
    CONSTRAINT FK_Specs_CPUs FOREIGN KEY (CPU_ID) REFERENCES CPUs(ID),
    CONSTRAINT FK_Specs_GPUs FOREIGN KEY (GPU_ID) REFERENCES GPUs(ID),
    CONSTRAINT FK_Specs_Storages FOREIGN KEY (Storage_ID) REFERENCES Storages(ID),
    CONSTRAINT FK_Specs_RAMs FOREIGN KEY (RAM_ID) REFERENCES RAMs(ID),
    CONSTRAINT FK_Specs_Screens FOREIGN KEY (Screen_ID) REFERENCES Screens(ID),
    CONSTRAINT FK_Specs_OSs FOREIGN KEY (OS_ID) REFERENCES OSs(ID)
)
"""

create_products_table_query = """
CREATE TABLE Products (
    ID INT,
    Name VARCHAR(50),
    Manufacturer_ID INT,
    Spec_ID INT,
    Category_ID INT,
    CONSTRAINT PK_Products PRIMARY KEY (ID),
    CONSTRAINT FK_Products_Manufacturers FOREIGN KEY (Manufacturer_ID) REFERENCES Manufacturers(ID),
    CONSTRAINT FK_Products_Specs FOREIGN KEY (Spec_ID) REFERENCES Specs(ID),
    CONSTRAINT FK_Products_Categories FOREIGN KEY (Category_ID) REFERENCES Categories(ID)
)
"""

create_prices_table_query = """
CREATE TABLE Prices (
    ID INT,
    Quantity INT,
    Price INT,
    Discount INT,
    Total_Price INT,
    Profit INT,
    Dollar_Price INT,
    Product_ID INT,
    CONSTRAINT PK_Prices PRIMARY KEY (ID),
    CONSTRAINT FK_Prices_Products FOREIGN KEY (Product_ID) REFERENCES Products(ID)
)
"""

create_orders_table_query = """
CREATE TABLE Orders (
    ID INT,
    Branch VARCHAR(31),
    Date DATE,
    Priority CHAR,
    Ship_Duration INT,
    Price_ID INT,
    CONSTRAINT PK_Orders PRIMARY KEY (ID),
    CONSTRAINT FK_Orders_Prices FOREIGN KEY (Price_ID) REFERENCES Prices(ID)
)
"""


my_db, my_cursor = connect_database(my_db, my_cursor, host, user, password, database)
my_cursor.execute(create_manufacturers_table_query)
my_cursor.execute(create_categories_table_query)
my_cursor.execute(create_CPUs_table_query)
my_cursor.execute(create_GPUs_table_query)
my_cursor.execute(create_storages_table_query)
my_cursor.execute(create_RAMs_table_query)
my_cursor.execute(create_screens_table_query)
my_cursor.execute(create_OSs_table_query)
my_cursor.execute(create_specs_table_query)
my_cursor.execute(create_products_table_query)
my_cursor.execute(create_prices_table_query)
my_cursor.execute(create_orders_table_query)
my_db.commit()
my_db, my_cursor = disconnect_database(my_db, my_cursor)

df = pd.read_csv(file_dir, low_memory=False)
df["Screen_Size"] = df["Screen_Size"].str.replace('"', "").astype(float)
df["RAM"] = df["RAM"].str.replace("GB", "").astype(int)
df["Weight"] = df["Weight"].replace(["kgs", "kg"], "", regex=True).astype(float)

# ------------------------------------------------------------------
# Dollar Price
df["Order_Date"] = df["Order_Date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").togregorian())

df_dollar_price = pd.read_csv(file_dir2, index_col=[0])
df_dollar_price["miladi"] = pd.to_datetime(df_dollar_price["miladi"])

df = pd.merge(
    df,
    df_dollar_price,
    how="left",
    left_on="Order_Date",
    right_on="miladi",
)
df.drop(columns=["miladi", "shamsi"], inplace=True)
df.rename(columns={"close_price": "Dollar_Price"}, inplace=True)
# ------------------------------------------------------------------


def set_index(_df):
    _df.insert(0, "ID", _df.index)
    return _df


def merge_df(
    df_left,
    df_right,
    col_name_left,
    col_name_right,
    col_name_from,
    col_name_to,
    other_cols=[],
):
    cols = col_name_left + col_name_right + other_cols
    df = pd.merge(
        df_left,
        df_right,
        how="left",
        left_on=col_name_left,
        right_on=col_name_right,
    )
    df.rename(columns={col_name_from: col_name_to}, inplace=True)
    df.drop(cols, axis=1, inplace=True)
    return df


# ----------------------------------------------------------------------------------------------------------
# Building a DataFrame of Database Tables

# ------------------------------------------------------------------
# Manufacturers Database
cpus = df["CPU"].unique()
gpus = df["GPU"].unique()
my_set = {item.split()[0] for sublist in [cpus, gpus] for item in sublist}
my_set = my_set | set(df["Manufacturer"].unique())
df_table_manufacturers = pd.DataFrame(my_set, columns=["Name"])
df_table_manufacturers = set_index(df_table_manufacturers)


# ------------------------------------------------------------------
# Categories Database
df_table_categories = pd.DataFrame(df["Category"].unique(), columns=["Name"])
df_table_categories = set_index(df_table_categories)


# ------------------------------------------------------------------
# CPUs Database
df_table_CPUs = pd.DataFrame(df["CPU"].unique(), columns=["Model"])
freq_regex_pattern = r"(\d+(\.\d+)?)(?= ?GHz)"
freq_ghz_regex_pattern = r"[\d\.]+GHz"
df_table_CPUs["Frequency"] = (
    df_table_CPUs["Model"]
    .str.extract(freq_regex_pattern, expand=False)[0]
    .astype(float)
)
df_table_CPUs["Manufacturer"] = df_table_CPUs["Model"].str.split().str[0]
df_table_CPUs["temp"] = df_table_CPUs["Model"]
df_table_CPUs["temp"] = df_table_CPUs["Model"]
df_table_CPUs["Model"] = df_table_CPUs.apply(
    lambda row: row["Model"].replace(row["Manufacturer"], "").strip(), axis=1
)
df_table_CPUs["Model"] = (
    df_table_CPUs["Model"]
    .str.replace(freq_ghz_regex_pattern, "", regex=True)
    .str.strip()
)
df_table_CPUs = merge_df(
    df_table_CPUs,
    df_table_manufacturers,
    ["Manufacturer"],
    ["Name"],
    "ID",
    "Manufacturer_ID",
)
df_table_CPUs = set_index(df_table_CPUs)


# ------------------------------------------------------------------
# GPUs Database
df_table_GPUs = pd.DataFrame(df["GPU"].unique(), columns=["Model"])
df_table_GPUs["Manufacturer"] = df_table_GPUs["Model"].str.split().str[0]
df_table_GPUs["temp"] = df_table_GPUs["Model"]
df_table_GPUs["Model"] = df_table_GPUs.apply(
    lambda row: row["Model"].replace(row["Manufacturer"], "").strip(), axis=1
)
df_table_GPUs = merge_df(
    df_table_GPUs,
    df_table_manufacturers,
    ["Manufacturer"],
    ["Name"],
    "ID",
    "Manufacturer_ID",
)
df_table_GPUs = set_index(df_table_GPUs)


# ------------------------------------------------------------------
# Storages Database
df_table_storages = pd.DataFrame(df["Storage"].unique(), columns=["Model"])
df_table_storages = set_index(df_table_storages)


# ------------------------------------------------------------------
# RAMs Database
df_table_RAMs = pd.DataFrame(df["RAM"].unique(), columns=["Size"])
df_table_RAMs = set_index(df_table_RAMs)


# ------------------------------------------------------------------
# Screens Database
df_table_screens = (
    df[["Screen_Size", "Screen"]].drop_duplicates().reset_index(drop=True)
)
df_table_screens.rename(columns={"Screen_Size": "Size", "Screen": "Type"}, inplace=True)
df_table_screens["Resolution"] = df_table_screens["Type"].str.extract(
    r"(\d{3,4}x\d{3,4})"
)
df_table_screens["temp"] = df_table_screens["Type"]
df_table_screens["Type"] = df_table_screens.apply(
    lambda row: row["Type"].replace(row["Resolution"], "").strip(), axis=1
)
df_table_screens = df_table_screens[["Size", "Resolution", "Type", "temp"]]
df_table_screens = set_index(df_table_screens)


# ------------------------------------------------------------------
# OSs Database
df_table_OSs = df[["OS", "OS_Version"]].drop_duplicates().reset_index(drop=True)
df_table_OSs.rename(columns={"OS": "Name", "OS_Version": "Version"}, inplace=True)
df_table_OSs = set_index(df_table_OSs)


# ------------------------------------------------------------------
df_products = df.drop(
    [
        "Order_ID",
        "Branch",
        "Order_Priority",
        "Order_Date",
        "Price",
        "Quantity",
        "Discount",
        "Total_Price",
        "Profit",
        "Dollar_Price",
        "Ship_Duration",
    ],
    axis=1,
)
df_products = df_products.drop_duplicates().reset_index(drop=True)
df_products = set_index(df_products)
# ------------------------------------------------------------------


# ------------------------------------------------------------------
# Prices Database
df_table_prices = merge_df(
    df,
    df_products,
    [
        "Manufacturer",
        "Model_Name",
        "Category",
        "Screen_Size",
        "Screen",
        "CPU",
        "RAM",
        "Storage",
        "GPU",
        "OS",
        "OS_Version",
        "Weight",
    ],
    [
        "Manufacturer",
        "Model_Name",
        "Category",
        "Screen_Size",
        "Screen",
        "CPU",
        "RAM",
        "Storage",
        "GPU",
        "OS",
        "OS_Version",
        "Weight",
    ],
    "ID",
    "Product_ID",
    ["Order_ID", "Branch", "Order_Date", "Order_Priority", "Ship_Duration"],
)
df_table_prices = df_table_prices.drop_duplicates().reset_index(drop=True)
df_table_prices = df_table_prices[
    [
        "Quantity",
        "Price",
        "Discount",
        "Total_Price",
        "Profit",
        "Dollar_Price",
        "Product_ID",
    ]
]
df_table_prices = set_index(df_table_prices)


# ------------------------------------------------------------------
# Orders Database
df_table_orders = merge_df(
    df,
    df_products,
    [
        "Manufacturer",
        "Model_Name",
        "Category",
        "Screen_Size",
        "Screen",
        "CPU",
        "RAM",
        "Storage",
        "GPU",
        "OS",
        "OS_Version",
        "Weight",
    ],
    [
        "Manufacturer",
        "Model_Name",
        "Category",
        "Screen_Size",
        "Screen",
        "CPU",
        "RAM",
        "Storage",
        "GPU",
        "OS",
        "OS_Version",
        "Weight",
    ],
    "ID",
    "Product_ID2",
)
df_table_orders = merge_df(
    df_table_orders,
    df_table_prices,
    [
        "Price",
        "Quantity",
        "Discount",
        "Total_Price",
        "Profit",
        "Dollar_Price",
        "Product_ID2",
    ],
    [
        "Price",
        "Quantity",
        "Discount",
        "Total_Price",
        "Profit",
        "Dollar_Price",
        "Product_ID",
    ],
    "ID",
    "Price_ID",
)
df_table_orders.rename(
    columns={
        "Order_ID": "ID",
        "Order_Date": "Date",
        "Order_Priority": "Priority",
    },
    inplace=True,
)


# ------------------------------------------------------------------
df_products = df_products.drop(["ID"], axis=1)
df_products = merge_df(
    df_products,
    df_table_OSs,
    ["OS", "OS_Version"],
    ["Name", "Version"],
    "ID",
    "OS_ID",
)
df_products = merge_df(
    df_products,
    df_table_categories,
    ["Category"],
    ["Name"],
    "ID",
    "Category_ID",
)
df_products = merge_df(
    df_products,
    df_table_screens,
    ["Screen_Size", "Screen"],
    ["Size", "temp"],
    "ID",
    "Screen_ID",
    ["Resolution", "Type"],
)
df_products = merge_df(
    df_products,
    df_table_CPUs,
    ["CPU"],
    ["temp"],
    "ID",
    "CPU_ID",
    ["Model", "Frequency", "Manufacturer_ID"],
)
df_products = merge_df(
    df_products,
    df_table_GPUs,
    ["GPU"],
    ["temp"],
    "ID",
    "GPU_ID",
    ["Model", "Manufacturer_ID"],
)
df_products = merge_df(
    df_products,
    df_table_RAMs,
    ["RAM"],
    ["Size"],
    "ID",
    "RAM_ID",
)
df_products = merge_df(
    df_products,
    df_table_storages,
    ["Storage"],
    ["Model"],
    "ID",
    "Storage_ID",
)
df_products = merge_df(
    df_products,
    df_table_manufacturers,
    ["Manufacturer"],
    ["Name"],
    "ID",
    "Manufacturer_ID",
)
df_products = set_index(df_products)
# ------------------------------------------------------------------


# ------------------------------------------------------------------
# Specs Database
df_table_specs = df_products[
    [
        "ID",
        "Weight",
        "CPU_ID",
        "GPU_ID",
        "Storage_ID",
        "RAM_ID",
        "Screen_ID",
        "OS_ID",
    ]
]


# ------------------------------------------------------------------
# Products Database
df_table_products = df_products[
    [
        "Model_Name",
        "Manufacturer_ID",
        "ID",
        "Category_ID",
    ]
]
df_table_products.rename(columns={"Model_Name": "Name", "ID": "Spec_ID"}, inplace=True)
df_table_products = set_index(df_table_products)


# my DataFrames: df, df_products, df_dollar_price

# my Database DataFrames:
# df_table_manufacturers, df_table_categories, df_table_CPUs,
# df_table_GPUs, df_table_storages, df_table_RAMs,
# df_table_screens, df_table_OSs, df_table_prices,
# df_table_orders, df_table_specs, df_table_products


engine = create_engine(
    url="mysql+pymysql://{0}:%s@{1}/{2}".format(user, host, database)
    % quote_plus(password)
)

df_table_manufacturers.to_sql(name="Manufacturers", con=engine, if_exists="append", index=False)
df_table_categories.to_sql(name="Categories", con=engine, if_exists="append", index=False)

df_table_CPUs = df_table_CPUs.drop(["temp"], axis=1)
df_table_CPUs.to_sql(name="CPUs", con=engine, if_exists="append", index=False)

df_table_GPUs = df_table_GPUs.drop(["temp"], axis=1)
df_table_GPUs.to_sql(name="GPUs", con=engine, if_exists="append", index=False)

df_table_storages.to_sql(name="Storages", con=engine, if_exists="append", index=False)
df_table_RAMs.to_sql(name="RAMs", con=engine, if_exists="append", index=False)

df_table_screens = df_table_screens.drop(["temp"], axis=1)
df_table_screens.to_sql(name="Screens", con=engine, if_exists="append", index=False)

df_table_OSs.to_sql(name="OSs", con=engine, if_exists="append", index=False)
df_table_specs.to_sql(name="Specs", con=engine, if_exists="append", index=False)
df_table_products.to_sql(name="Products", con=engine, if_exists="append", index=False)
df_table_prices.to_sql(name="Prices", con=engine, if_exists="append", index=False)

df_table_orders.to_sql(name="Orders", con=engine, if_exists="append", index=False)