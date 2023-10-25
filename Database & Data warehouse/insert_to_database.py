import mysql.connector
import pandas as pd
import numpy as np

# connecting to mysql server
mydb = mysql.connector.connect(
    host='', 
    username= '',
    password= ''
)

# creating the curser
mycursor = mydb.cursor()

# reading the CSV file
df = pd.read_csv('sales_data.csv')

# replacing nulls with no_info
df.replace(np.nan, 'no_info', inplace=True)

# using the database
mycursor.execute('USE last_project;')

# inserting data into Manufacturers, Catefories, Screens, RAMs, Storages and OSs

Manufacturers1 = set(df['Manufacturer'].unique())
Manufacturers2 = set([x.split()[0] for x in df['CPU'].values])
Manufacturers3 = set([x.split()[0] for x in df['GPU'].values])
Manufacturers = Manufacturers1 | Manufacturers2 | Manufacturers3
Categories = df['Category'].unique()
OSs = set([tuple(x) for x in df[['OS', 'OS_Version']].values])
Screens = set([(x[:-1], y[:-9].strip(), y[-9:]) for x, y in df[['Screen_Size', 'Screen']].values])
RAMs = [x[:-2] for x in df['RAM'].unique()]
Storages = [(x.split()[0], x.split()[1]) for x in df['Storage'].unique()]

for Manufacturer in Manufacturers:
    query = 'INSERT INTO Manufacturers (Name) VALUES (%s)'
    data = [Manufacturer] 
    mycursor.execute(query, data)
mydb.commit()
for Category in Categories:
    query = 'INSERT INTO Categories (Name) VALUES (%s)'
    data = [Category] 
    mycursor.execute(query, data)
mydb.commit()
for a,b in OSs:
    query = 'INSERT INTO OSs (Name, Version) VALUES (%s, %s)'
    data = [a, b] 
    mycursor.execute(query, data)
mydb.commit()
for a,b,c in Screens:
    query = 'INSERT INTO Screens (Size, Type, Resolution) VALUES (%s, %s, %s)'
    data = [a, b, c] 
    mycursor.execute(query, data)
mydb.commit()
for ram in RAMs:
    query = 'INSERT INTO RAMs (size) VALUES (%s)'
    data = [ram] 
    mycursor.execute(query, data)
mydb.commit()

# inserting data into CPUs and GPUs

query = ''' SELECT * FROM Manufacturers;'''
df_manufacturers = pd.read_sql(query, mydb)
df_cpu_manufacturer = pd.DataFrame([(x.split()[0], x.replace(x.split()[-1], '').replace(x.split()[0], '').strip(), x.split()[-1]) for x in df['CPU'].values], columns=['cpu_manufacturer', 'model', 'frequency'])
df_cpu_manufacturer = pd.merge(df_manufacturers, df_cpu_manufacturer, right_on='cpu_manufacturer', left_on='Name')
cpus = set([(x, y, z[:-3]) for x, y, z in df_cpu_manufacturer[['ID', 'model', 'frequency']].values])
df_gpu_manufacturer = pd.DataFrame([(x.split()[0], x.replace(x.split()[0], '').strip()) for x in df['GPU'].values], columns=['gpu_manufacturer', 'model'])
df_gpu_manufacturer = pd.merge(df_manufacturers, df_gpu_manufacturer, left_on='Name', right_on='gpu_manufacturer')
gpus = set([(x, y) for x, y in df_gpu_manufacturer[['model', 'ID']].values])

for a,b,c in cpus:
    query = 'INSERT INTO CPUs (Manufacturer_ID, Model, Frequency) VALUES (%s, %s, %s)'
    data = [a, b, c] 
    mycursor.execute(query, data)
mydb.commit()
for a,b in gpus:
    query = 'INSERT INTO GPUs (Model, Manufacturer_ID) VALUES (%s, %s)'
    data = [a, b] 
    mycursor.execute(query, data)
mydb.commit()


