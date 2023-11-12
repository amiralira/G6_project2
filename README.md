# Laptop Market Analytics Dashboard

## Overview
This project involves a dataset of sales and orders from a laptop importing company, containing information such as Order_ID, Branch, Order_Date, Order_Priority, Manufacturer, Model_Name, Category, Screen_Size, Screen, CPU, RAM, Storage, GPU, OS, OS_Version, Weight, Price, Quantity, Discount, Total_Price, Profit, and Ship_Duration. The dataset includes 1,017,081 recorded orders spanning from the year 1390 to 1402 (Solar Hijri calendar).

Note: Due to high inflation rates in Iran and the fluctuating value of the Toman/Rial relative to the dollar, we used a more stable exchange rate for our analysis. Additionally, laptop manufacturers have specific production policies for each year, producing models with varying price ranges. To facilitate our analysis, we obtained the USD to Toman/Rial exchange rates from a specific API based on the order dates. It's important to consider that some dates may lack exchange rates due to official market closures, in which case, we use the previous day's rate.

## Data Normalization and Database Design
After examining the available data, the first step is to store the data in a normalized and structured way in the database. Entity identification is performed, and tables are designed based on these entities. Each entity has attributes that name the columns of each table. Relationships between tables are established for optimal join performance, considering time efficiency. Unique values are stored in each table to address the high complexity in the dataset.

![Database Structure](Image%20Results/Database.png)

## Data Warehouse and Power BI
Following the design and storage of data in the database, the next step is to design a suitable data warehouse. Power BI is used for this purpose, employing the Star schema design principle. Fact tables, containing transaction-oriented data with a large volume, are utilized, while Dimension tables contain descriptive data.

![Data Warehouse Schema](Image%20Results/Data%20Warehouse.png)

## Competitor Analysis
The project involves extracting data from competitors' websites to identify and complete missing products. Additionally, pricing strategies and current company policies are analyzed for potential adjustments.

Competitor information is available at [link1](https://drive.google.com/file/d/1k8ipAY1gLrC8c4F18uTgFvdbwYgWrMHS/view?usp=drive_link), [link2](https://drive.google.com/file/d/1aE236RzcdJz4jPweipJyP4wfy5Mckhp9/view?usp=drive_link).

## Dashboard Creation
To meet the company's needs, a dashboard is created to display the current status of the company and address specific requests. Power BI is employed for dashboard creation.

Download the Power BI output at [link](https://drive.google.com/file/d/1XYj-5oTi0P42MDWHzWfQuU23G3m0W1dF/view?usp=drive_link).

### Request 1: Targeted Advertising
To increase customer base, the company plans to allocate a budget for advertising. We recommend cities with higher sales relative to their population and better profitability for targeted advertising.

![Advertising Recommendation1](Image%20Results/Request%201-1.png)
![Advertising Recommendation2](Image%20Results/Request%201-2.png)

### Request 2: Impact of Discounts on Sales
The company wants to assess if discounts affect sales and how. T-tests are used to determine the significance of these effects. Data is divided into two sections: with and without discounts, and the average sales in both sections are compared.

![Discount Impact1](Image%20Results/Request%202-1.png)
![Discount Impact2](Image%20Results/Request%202-2.png)

### Request 3: Impact of Discounts on Profit
Building on the previous request, the company is concerned about potential profit reductions due to discounts. The average profitability is used for dashboard representation, especially during high-cash-volume orders.

![Profit Impact1](Image%20Results/Request%203-1.png)
![Profit Impact2](Image%20Results/Request%203-2.png)

### Request 4: Capital Allocation for New Laptops
The company seeks advice on allocating capital among different laptop brands and categories. Profitability for each brand in specific categories is calculated, and 20% of the profit is considered for product import and inventory completion.

![Capital Allocation](Image%20Results/Request%204.png)

### Request 5: Price Prediction for New Laptops
Considering the company's return to the market after a long period, it needs a solution for predicting laptop prices based on technical specifications. Machine learning techniques are applied to predict prices based on influential features.

![Price Prediction](Image%20Results/Request%205.png)

### Request 6: Monthly Sales Analysis
The company plans to import goods monthly and wants to know if there is a difference in sales across different months. If differences exist, the company seeks guidance on how to allocate its annual budget among these months.

To address this request, a prediction is made that sales may perform well in months at the end of the year or the beginning of the following year (e.g., Esfand and Farvardin). The popularity of sales in each month is determined based on obtained outputs, aligning with predictions.

![Monthly Sales Analysis](Image%20Results/Request%206.png)

### Request 7: Importance of Priority Levels
In the past, the company had a policy favoring certain priority levels, impacting various aspects such as shipping methods. However, this policy has proven challenging. The company requests an assessment of whether maintaining this policy is justified based on the average profitability under these conditions.

From the obtained average profitability results, it is evident that high priority levels or short order durations have a minimal impact on profitability.

![Priority Levels Impact](Image%20Results/Request%207.png)

### Request 8: Key Factor in Customer Laptop Purchases
Examine which laptop feature is the most crucial factor for customer purchases.

To answer this request, it is essential to consider that the most critical factor during purchases is the price. Eliminating its influence allows us to identify other features that attract or repel customers. For instance, an increase in CPU frequency, screen resolution, or RAM size may attract more customers, while an increase in weight or screen size may deter them.

![Key Factor in Purchases](Image%20Results/Request%208.png)

### Request 9: Alerting System Based on KPI

In this section, an alerting system is implemented based on Key Performance Indicators (KPI) and predefined thresholds. It compares the average sales for past years or months with the current year or month. If the average falls below the threshold, an alert is triggered, indicating a warning state. Conversely, if it exceeds the threshold, it signifies a stable state.

The current status is undetermined for the current year as the sales data for the current year is incomplete. However, for the current month, the system indicates a stable state.

![Alerting System Based on KPI](Image%20Results/Request%209.png)


## Detailed Analysis in the First Dashboard

### Monthly, Seasonal, and Annual Sales
Total sales are examined for the current month, season, and year, both in dollars and Iranian rials.

![Dashboard1](Image%20Results/Dashboard%201-1-1.png)
![Dashboard1](Image%20Results/Dashboard%201-1-2-1.png)
![Dashboard1](Image%20Results/Dashboard%201-1-2-2.png)
![Dashboard1](Image%20Results/Dashboard%201-1-3.png)

### Monthly, Seasonal, and Annual Profits
Total profits are analyzed for the current month, season, and year, both in dollars and Iranian rials.

![Dashboard1](Image%20Results/Dashboard%201-2-1.png)
![Dashboard1](Image%20Results/Dashboard%201-2-2.png)
![Dashboard1](Image%20Results/Dashboard%201-2-3.png)

### Total Sales and Profits Across Different Cities
Sales and profits are evaluated across various cities, presented in both dollars and Iranian rials.

![Dashboard1](Image%20Results/Dashboard%201-3.png)

### Sales and Profit Trends Over Time in Specific Cities
A dynamic menu allows managers to select specific cities, years, months, and days to observe the changing trends in sales and profits.

![Dashboard1](Image%20Results/Dashboard%201-4-1.gif)
![Dashboard1](Image%20Results/Dashboard%201-4-3-1.png)
![Dashboard1](Image%20Results/Dashboard%201-4-3-2.png)
![Dashboard1](Image%20Results/Dashboard%201-4-2.gif)

### Sales and Profit Trends Over Time Based on Laptop Brands or Categories
Another menu enables managers to choose specific laptop brands and categories to visualize changing trends.

![Dashboard1](Image%20Results/Dashboard%201-5-1-2.png)
![Dashboard1](Image%20Results/Dashboard%201-5-1-1.png)
![Dashboard1](Image%20Results/Dashboard%201-5-2.png)
![Dashboard1](Image%20Results/Dashboard%201-5-3.png)
![Dashboard1](Image%20Results/Dashboard%201-5-4.png)


## Detailed Analysis in the Second Dashboard

In this section, a menu is provided for the user to select specific cities and time intervals (month and year). Based on the user's selection, various outputs are updated accordingly.

1. **Overview of Sales, Orders, and Averages:**
   The total sales, order count, average profit of all orders, and the average sales and profit of all orders are displayed based on the user's selected criteria.
   ![Dashboard2](Image%20Results/Dashboard%202-1.png)

2. **Popularity of Brands and Categories:**
   The popularity of each brand and category is visualized to provide insights into customer preferences.
   ![Dashboard2](Image%20Results/Dashboard%202-2.png)

3. **Popularity of CPU and GPU Models:**
   The popularity of each CPU and GPU model is depicted to understand customer preferences in terms of hardware.
   ![Dashboard2](Image%20Results/Dashboard%202-3.png)

4. **Order Priority and RAM Size Popularity:**
   The priority of orders and the popularity of RAM sizes are illustrated to help identify trends in customer choices.
   ![Dashboard2](Image%20Results/Dashboard%202-4.png)

5. **Sales and Order Count by Province:**
   The sales and order count are presented for each province, offering a regional perspective.
   ![Dashboard2](Image%20Results/Dashboard%202-5.png)

6. **Impact of Discounts on Sales Count:**
   The effect of discounts on the number of sales is highlighted, providing insights into customer behavior.
   ![Dashboard2](Image%20Results/Dashboard%202-6.png)

7. **Popularity of Screen Sizes:**
   The popularity of different screen sizes is visualized to understand customer preferences.
   ![Dashboard2](Image%20Results/Dashboard%202-7.png)

8. **Order Dispersion by Laptop Price:**
   The dispersion of orders based on laptop prices is showcased, revealing the distribution of customer preferences.
   ![Dashboard2](Image%20Results/Dashboard%202-8.png)
