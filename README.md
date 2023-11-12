# G6_project2
This Project has multiple phases starting with:
1. Creating Database
2. Analysis and Review of Competitors
3. Creating Data Warehouses
4. Analyzing Different Scenarios Statistically 
5. Power-BI:
   https://drive.google.com/file/d/1bkzuwRkYeRhpaBYqhPly4DQ6SHI8unGI/view?usp=drive_link
6. Trello Link:
   https://trello.com/b/gh2cF6AI/first-quera-project



# Project Description

## Overview
This project involves a dataset of sales and orders from a laptop importing company, containing information such as Order_ID, Branch, Order_Date, Order_Priority, Manufacturer, Model_Name, Category, Screen_Size, Screen, CPU, RAM, Storage, GPU, OS, OS_Version, Weight, Price, Quantity, Discount, Total_Price, Profit, and Ship_Duration. The dataset includes 1,017,081 recorded orders spanning from the year 1390 to 1402 (Solar Hijri calendar).

Note: Due to high inflation rates in Iran and the fluctuating value of the Toman/Rial relative to the dollar, we used a more stable exchange rate for our analysis. Additionally, laptop manufacturers have specific production policies for each year, producing models with varying price ranges. To facilitate our analysis, we obtained the USD to Toman/Rial exchange rates from a specific API based on the order dates. It's important to consider that some dates may lack exchange rates due to official market closures, in which case, we use the previous day's rate.

## Data Normalization and Database Design
After examining the available data, the first step is to store the data in a normalized and structured way in the database. Entity identification is performed, and tables are designed based on these entities. Each entity has attributes that name the columns of each table. Relationships between tables are established for optimal join performance, considering time efficiency. Unique values are stored in each table to address the high complexity in the dataset.

![Database Structure](https://github.com/amiralira/G6_project2/blob/main/Image%20Results/Database.png)

## Data Warehouse and Power BI
Following the design and storage of data in the database, the next step is to design a suitable data warehouse. Power BI is used for this purpose, employing the Star schema design principle. Fact tables, containing transaction-oriented data with a large volume, are utilized, while Dimension tables contain descriptive data.

![Data Warehouse Schema](https://github.com/amiralira/G6_project2/blob/main/Image%20Results/Data%20Warehouse.png)

## Competitor Analysis
The project involves extracting data from competitors' websites to identify and complete missing products. Additionally, pricing strategies and current company policies are analyzed for potential adjustments.

Competitor information is available at ![link1](https://drive.google.com/file/d/1k8ipAY1gLrC8c4F18uTgFvdbwYgWrMHS/view?usp=drive_link), ![link2](https://drive.google.com/file/d/1aE236RzcdJz4jPweipJyP4wfy5Mckhp9/view?usp=drive_link).

## Dashboard Creation
To meet the company's needs, a dashboard is created to display the current status of the company and address specific requests. Power BI is employed for dashboard creation.

Download the Power BI output at [link](power_bi_link).

### Request 1: Targeted Advertising
To increase customer base, the company plans to allocate a budget for advertising. We recommend cities with higher sales relative to their population and better profitability for targeted advertising.

![Advertising Recommendation](link_to_image)

### Request 2: Impact of Discounts on Sales
The company wants to assess if discounts affect sales and how. T-tests are used to determine the significance of these effects. Data is divided into two sections: with and without discounts, and the average sales in both sections are compared.

![Discount Impact](link_to_image)

### Request 3: Impact of Discounts on Profit
Building on the previous request, the company is concerned about potential profit reductions due to discounts. The average profitability is used for dashboard representation, especially during high-cash-volume orders.

![Profit Impact](link_to_image)

### Request 4: Capital Allocation for New Laptops
The company seeks advice on allocating capital among different laptop brands and categories. Profitability for each brand in specific categories is calculated, and 20% of the profit is considered for product import and inventory completion.

![Capital Allocation](link_to_image)

### Request 5: Price Prediction for New Laptops
Considering the company's return to the market after a long period, it needs a solution for predicting laptop prices based on technical specifications. Machine learning techniques are applied to predict prices based on influential features.

![Price Prediction](link_to_image)
