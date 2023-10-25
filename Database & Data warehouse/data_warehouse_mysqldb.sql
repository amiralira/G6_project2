CREATE DATABASE IF NOT EXISTS datawarehouse;
USE datawarehouse;
-- USE project2;

-- if your database name is project2 use project2. else change it


CREATE TABLE ProductFactTable AS
SELECT
    P.ID AS Product_ID,
    O.ID AS Order_ID,
    Prc.ID AS Price_ID,
    P.Name,
    M.Name AS Manufacturer,
    C.Name AS Category,
    R.Size AS RAM,
    S.Model AS Storage,
    Sp.Weight
FROM
    project2.Orders O
JOIN
    project2.Prices Prc ON O.Price_ID = Prc.ID
JOIN
    project2.Products P ON Prc.Product_ID = P.ID
JOIN
    project2.Manufacturers M ON P.Manufacturer_ID = M.ID
JOIN
    project2.Categories C ON P.Category_ID = C.ID
JOIN
    project2.Specs Sp ON P.Spec_ID = Sp.ID
JOIN
    project2.RAMs R ON Sp.RAM_ID = R.ID
JOIN
    project2.Storages S ON Sp.Storage_ID = S.ID;


CREATE TABLE ProductDimension AS
SELECT
    P.ID AS Product_ID,
    CPU_M.Name AS CPU_Manufacturer,
    CPU.Model AS CPU_Model,
    CPU.Frequency AS CPU_Freq,
    GPU_M.Name AS GPU_Manufacturer,
    GPU.Model AS GPU_Model,
    OS.Name AS OS_Name,
    OS.Version AS OS_Version,
    Sc.Size AS Screen_Size,
    Sc.Resolution AS Screen_Resolution,
    Sc.Type AS Screen_Type
FROM
    project2.Products P
JOIN
    project2.Specs Sp ON P.Spec_ID = Sp.ID
LEFT JOIN
    project2.CPUs CPU ON Sp.CPU_ID = CPU.ID
LEFT JOIN
    project2.Manufacturers CPU_M ON CPU.Manufacturer_ID = CPU_M.ID
LEFT JOIN
    project2.GPUs GPU ON Sp.GPU_ID = GPU.ID
LEFT JOIN
    project2.Manufacturers GPU_M ON GPU.Manufacturer_ID = GPU_M.ID
LEFT JOIN
    project2.OSs OS ON Sp.OS_ID = OS.ID
LEFT JOIN
    project2.Screens Sc ON Sp.Screen_ID = Sc.ID;


CREATE TABLE OrdersDimension AS
SELECT
    O.ID AS Order_ID,
    O.Branch AS Order_Branch,
    O.Date AS Order_Date,
    O.Priority AS Order_Priority,
    O.Ship_Duration AS Ship_Duration
FROM
    project2.Orders O;


CREATE TABLE PriceDimension AS
SELECT
    Prc.ID AS Price_ID,
    Prc.Quantity,
    Prc.Price,
    Prc.Discount,
    Prc.Total_Price,
    Prc.Profit,
    Prc.Dollar_Price
FROM
    project2.Prices Prc;


ALTER TABLE OrdersDimension
ADD PRIMARY KEY (Order_ID);

ALTER TABLE PriceDimension
ADD PRIMARY KEY (Price_ID);

ALTER TABLE ProductDimension
-- ADD CONSTRAINT FK_ProductDimension_Products FOREIGN KEY (Product_ID) REFERENCES ProductFactTable(Product_ID),
ADD PRIMARY KEY (Product_ID);

ALTER TABLE ProductFactTable
ADD CONSTRAINT FK_ProductFactTable_Orders FOREIGN KEY (Order_ID) REFERENCES OrdersDimension(Order_ID),
ADD CONSTRAINT FK_ProductFactTable_Prices FOREIGN KEY (Price_ID) REFERENCES PriceDimension(Price_ID),
ADD CONSTRAINT FK_ProductFactTable_Products FOREIGN KEY (Product_ID) REFERENCES ProductDimension(Product_ID);
-- ADD PRIMARY KEY (Product_ID);