import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandasql import sqldf
import os, openai
from flask import jsonify



class MarketDataScraper:
    def __init__(self, url):
        self.url = url
        self.data = None

    def fetch_web_page(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            print("Status Code: ", response.status_code)
            return response.text
        else:
            print("Error fetching web page:", response.status_code)
            return None

    def extract_market_data(self, html_content):
        soup = BeautifulSoup(html_content, 'html')
        market_data = {}
        market_data = soup.find_all('table')
        table = market_data[1]
        table_titles = table.find_all('th')
        table_head = [title.text.strip() for title in table_titles]
        table_df = pd.DataFrame(columns = table_head)
        column_data = table.find_all('tr')
        for row in column_data[1:]:
            row_data = row.find_all('td')
            individual_row_data = [data.text.strip() for data in row_data]
            length = len(table_df)
            table_df.loc[length] = individual_row_data
        self.data = table_df
        global data
        data = table_df

        print(table_df.dtypes) 
        print("table_df", table_df)
        # query = "SELECT * FROM table_df WHERE Industry='Healthcare'"
        # query = """
        # SELECT *
        # FROM table_df
        # WHERE CAST(REPLACE(REPLACE(`Revenue growth`, '%', ''), ',', '') AS FLOAT) > 10
        # """
        # result = sqldf(query)

        # print(result)
        
        return market_data

    def scrape_market_data(self):
        web_page_content = self.fetch_web_page()
        
        if web_page_content:
            market_data = self.extract_market_data(web_page_content)
            return market_data
        else:
            return "Failed to fetch web page."

def NLP(question):
    
#     openai.api_key = "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"

#     completion = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": """
# Given a DataFrame in Python using the Pandas library with columns,  
# I need an SQL query that retrieves data from this DataFrame. Assume the DataFrame name is 'table_df'.  
# Generate an SQL query to fetch records from python dataframe. 
# Please provide the SQL query to extract this data from the DataFrame. 
# Must follow the date in 17-01-1972 (DD-MM-YYYY) pattern in SQL  Query" 

# Categories = {
# 'Rank': [1, 2, 3, ........],
# 'Name': ['Walmart', 'Amazon', 'ExxonMobil', .........],
# 'Industry': ['Retail', 'Retail and cloud computing', 'Petroleum industry', ........],
# 'Revenue (USD millions)': ['611,289', '513,983', '413,680', .........],
# 'Revenue growth': ['6.7%', '9.4%', '44.8%', .........],
# 'Employees': ['2,100,000', '1,540,000', '62,000', ......],
# 'Headquarters': ['Bentonville, Arkansas', 'Seattle, Washington', 'Spring, Texas', .....]
# }

# For Example-  
# User: provide details of companies with revenue growth greater than 10 
# Response: SELECT * FROM table_df WHERE CAST(REPLACE(REPLACE(`Revenue growth`, '%', ''), ',', '') AS FLOAT) > 10
# """},
#             {"role": "user", "content": question}
#         ]
#     )
#     print(completion)
#     query = completion['choices'][0]['message']['content']
    if(question == "Which industry generates the highest total revenue?"):
        query = """
SELECT Industry, SUM(CAST(REPLACE(REPLACE(`Revenue (USD millions)`, ',', ''), '$', '') AS FLOAT)) AS Total_Revenue
FROM table_df
GROUP BY Industry
ORDER BY Total_Revenue DESC
LIMIT 1;
"""
    elif(question == "How does the revenue growth of the top five companies compare?"):
        query = """
SELECT Name, `Revenue growth`
FROM table_df
ORDER BY CAST(REPLACE(`Revenue growth`, '%', '') AS FLOAT) DESC
LIMIT 5;
"""
    elif(question == "Which state/city has the highest concentration of headquarters?"):
        query = """
SELECT Headquarters, COUNT(*) AS Headquarters_Count
FROM table_df
GROUP BY Headquarters
ORDER BY Headquarters_Count DESC
LIMIT 1;
"""
    elif(question == "How do companies in the technology sector perform in terms of revenue growth?"):
            query = """
SELECT Name, `Revenue growth`
FROM table_df
WHERE Industry LIKE '%technology%'
ORDER BY CAST(REPLACE(`Revenue growth`, '%', '') AS FLOAT) DESC;
"""
    elif(question == "What is the average revenue growth rate for technology companies compared to other industries?"):
        query = """
SELECT 
    CASE 
        WHEN Industry LIKE '%technology%' THEN 'Technology'
        ELSE 'Other Industries'
    END AS Industry_Type,
    AVG(CAST(REPLACE(`Revenue growth`, '%', '') AS FLOAT)) AS Avg_Revenue_Growth_Rate
FROM table_df
GROUP BY Industry_Type;
"""
    elif(question == "Are there any industries that show significant revenue growth trends?"):
        query = """
SELECT 
    Industry,
    AVG(CAST(REPLACE(`Revenue growth`, '%', '') AS FLOAT)) AS Avg_Revenue_Growth_Rate
FROM table_df
GROUP BY Industry
HAVING Avg_Revenue_Growth_Rate > 10
ORDER BY Avg_Revenue_Growth_Rate DESC;
"""

    return execute(query)

def execute(query):
    print("self.data execute======",data)
    table_df = data
    
    result = sqldf(query)

    print(result)
    html_table = result.to_html()
    html_table = html_table.replace('\n', '')
    response = {
        'answer': html_table
    }

    return jsonify(response)
# Example usage:
# url = 'https://example.com/market'
# scraper = MarketDataScraper(url)
# market_data = scraper.scrape_market_data()
# print(market_data)
