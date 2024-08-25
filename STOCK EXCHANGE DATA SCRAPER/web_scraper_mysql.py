import warnings
import re
import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime 

class Scrap:

    def __init__(self):
        self.company_names = []
        self.base_url = None
        self.urls = []
        self.html_contents = []
        self.soups = []
        self.elements = None
        self.all_data = []
        self.data = {}
        self.db_connection = None
        self.cursor = None

    def connect_to_database(self):
        self.db_connection = mysql.connector.connect(
            host='localhost',
            user='stock_user',
            password='your_password',
            database='stock_data'
        )
        self.cursor = self.db_connection.cursor()

    def close_database_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.db_connection:
            self.db_connection.close()

    def get_company_names(self):
        self.company_names = []
        print("Enter company names one by one. Type 'done' when you are finished:")
        while True:
            company_name = input("Enter Company Name: ")
            if company_name.lower() == 'done':
                break
            self.company_names.append(company_name)

    def get_base_url(self):
        self.base_url = 'https://www.dsebd.org/displayCompany.php?name='

    def construct_urls(self):
        self.urls = []
        for company in self.company_names:
            url = f"{self.base_url}{company}"
            self.urls.append(url)

    def fetch_webpage_content(self):
        self.html_contents = []
        for url in self.urls:
            response = requests.get(url)
            self.html_contents.append(response.text)

    def initialize_beautifulsoup(self):
        self.soups = [BeautifulSoup(html, 'html.parser') for html in self.html_contents]

    def elements_for_search(self):
        self.elements = {
            'last_trading_price': 'Last Trading Price',
            'opening_price': 'Opening Price',
            'adjusted_opening_price': 'Adjusted Opening Price',
            'yesterday_closing_price': 'Yesterday\'s Closing Price',
            'closing_price': 'Closing Price',
            'days_range': 'Day\'s Range',
            '52_weeks_range': '52 Weeks\' Moving Range',
            'day_volume': 'Day\'s Volume \(Nos.\)',
            'day_trade': 'Day\'s Trade \(Nos.\)',
            'market_capitalization': 'Market Capitalization \(mn\)'
        }

    def suppress_deprecation_warning(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

    def extract_company_name(self):
        company_name_tag = self.soup.find('h2', class_='BodyHead topBodyHead')
        if company_name_tag:
            company_name_i_tag = company_name_tag.find('i')
            if company_name_i_tag:
                self.data['company_name'] = company_name_i_tag.get_text(strip=True)
            else:
                self.data['company_name'] = None
        else:
            self.data['company_name'] = None

    def extract_date(self):
        date_tag = self.soup.find('i', text=re.compile(r'\w+ \d{1,2}, \d{4}'))
        if date_tag:
            date_str = date_tag.get_text(strip=True)
            try:
                # Convert the date string to a datetime object
                date_obj = datetime.strptime(date_str, '%b %d, %Y')
                # Convert to MySQL-compatible date string format
                self.data['date'] = date_obj.strftime('%Y-%m-%d')
            except ValueError:
                self.data['date'] = None
        else:
            self.data['date'] = None

    def extract_data_using_beautifulsoup(self):
        for key, regex_pattern in self.elements.items():
            th_tag = self.soup.find('th', text=re.compile(regex_pattern, re.IGNORECASE))
            if th_tag:
                td_tag = th_tag.find_next_sibling('td')
                if td_tag:
                    value = td_tag.get_text(strip=True)
                    value = value.replace(',', '')
                    # Check if the value is '-', and convert it to None
                    self.data[key] = None if value == '-' else value
                else:
                    self.data[key] = None
            else:
                self.data[key] = None

    def extract_data_from_each_url_and_store(self):
        self.all_data = []
        for soup in self.soups:
            self.soup = soup
            self.data = {}
            self.extract_company_name()
            self.extract_date()
            self.extract_data_using_beautifulsoup()
            self.all_data.append(self.data.copy())

    def print_extracted_data(self):
        for i, data in enumerate(self.all_data):
            print(f"\nData from company {i+1} ({self.company_names[i]}):")
            for key, value in data.items():
                print(f"  {key}: {value}")
            print("\n")

    def write_data_to_database(self):
        for data in self.all_data:
            sql = """
            INSERT INTO stock_info (
                company_name, date, last_trading_price, opening_price, adjusted_opening_price, 
                yesterday_closing_price, closing_price, days_range, weeks_52_range, 
                day_volume, day_trade, market_capitalization
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                data['company_name'], data['date'], data.get('last_trading_price'), data.get('opening_price'),
                data.get('adjusted_opening_price'), data.get('yesterday_closing_price'), data.get('closing_price'),
                data.get('days_range'), data.get('52_weeks_range'), data.get('day_volume'),
                data.get('day_trade'), data.get('market_capitalization')
            )
            self.cursor.execute(sql, values)
            self.db_connection.commit()
        
        print("Data saved in MySQL database.")
        
    def run(self):
        self.get_company_names()
        self.get_base_url()
        self.construct_urls()
        self.fetch_webpage_content()
        self.initialize_beautifulsoup()
        self.elements_for_search()
        self.suppress_deprecation_warning()
        self.extract_data_from_each_url_and_store()
        self.connect_to_database()
        self.print_extracted_data()
        self.write_data_to_database()
        self.close_database_connection()

if __name__ == '__main__':
    ExtractData = Scrap()
    ExtractData.run()
