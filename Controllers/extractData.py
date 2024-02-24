import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandasql import sqldf
import os, openai
from flask import jsonify
from dotenv import load_dotenv

load_dotenv()

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
        
        return market_data

    def scrape_market_data(self):
        web_page_content = self.fetch_web_page()
        
        if web_page_content:
            market_data = self.extract_market_data(web_page_content)
            return market_data
        else:
            return "Failed to fetch web page."

def NLP(question):
    
    openai.api_key = os.getenv("OPENAI_API_KEY")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """
Given a DataFrame in Python using the Pandas library with columns,  
I need an SQL query that retrieves data from this DataFrame. Assume the DataFrame name is 'table_df'.  
Generate an SQL query to fetch records from python dataframe. 
Please provide the SQL query to extract this data from the DataFrame. 
Must follow the date in 17-01-1972 (DD-MM-YYYY) pattern in SQL  Query" 

Categories = {
'Rank': [1, 2, 3, ........],
'Name': ['Walmart', 'Amazon', 'ExxonMobil', .........],
'Industry': ['Retail', 'Retail and cloud computing', 'Petroleum industry', ........],
'Revenue (USD millions)': ['611,289', '513,983', '413,680', .........],
'Revenue growth': ['6.7%', '9.4%', '44.8%', .........],
'Employees': ['2,100,000', '1,540,000', '62,000', ......],
'Headquarters': ['Bentonville, Arkansas', 'Seattle, Washington', 'Spring, Texas', .....]
}

For Example-  
User: provide details of companies with revenue growth greater than 10 
Response: SELECT * FROM table_df WHERE CAST(REPLACE(REPLACE(`Revenue growth`, '%', ''), ',', '') AS FLOAT) > 10
"""},
            {"role": "user", "content": question}
        ]
    )
    print(completion)
    query = completion['choices'][0]['message']['content']
   

    return execute(query)

def execute(query):
    print("self.data execute======",data)
    table_df = data
    
    result = sqldf(query)

    print(result)
    
# Define CSS styles
    table_style = """
        <style>
        table {
            border-collapse: collapse;
            width: inherit;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        </style>
    """

    # Construct HTML table
    html_table = table_style + "<table><tr>"
    # Adding table headers
    for column in result.columns:
        html_table += f"<th>{column}</th>"
    html_table += "</tr>"

    # Adding table rows
    for index, row in result.iterrows():
        html_table += "<tr>"
        for value in row:
            html_table += f"<td>{value}</td>"
        html_table += "</tr>"
    html_table += "</table>"

    response = {
        'answer': html_table
    }

    return jsonify(response)

