import csv
import warnings
import re
import requests
from bs4 import BeautifulSoup

class Scrap:

    def __init__(self):
        self.urls = []
        self.html_contents = []
        self.soups = []
        self.elements = None
        self.all_data = []
        self.data = {}

    def get_urls(self):
        self.urls = [
            'https://www.dsebd.org/displayCompany.php?name=LHBL',
            'https://www.dsebd.org/displayCompany.php?name=AMBEEPHA',
            'https://www.dsebd.org/displayCompany.php?name=BATBC'
        ]

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
            self.data['date'] = date_tag.get_text(strip=True)
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
                    self.data[key] = value
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

    def write_data_to_csv_file(self):
        #Specify the CSV file name
        csv_file_name = 'extracted_data.csv'
        # Write data to CSV file
        with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['company_name', 'date'] + list(self.elements.keys())
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for data in self.all_data:
                writer.writerow(data)
        print(f"Data has been written to {csv_file_name}")

    def run(self):
        self.get_urls()
        self.fetch_webpage_content()
        self.initialize_beautifulsoup()
        self.elements_for_search()
        self.suppress_deprecation_warning()
        self.extract_data_from_each_url_and_store()
        self.write_data_to_csv_file()

if __name__ == '__main__':
    ExtractData = Scrap()
    ExtractData.run()