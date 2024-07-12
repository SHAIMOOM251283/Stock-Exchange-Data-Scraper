import warnings
import re
import requests
from bs4 import BeautifulSoup

class Scrap:

    def __init__(self):
        self.url = None
        self.html_content = None
        self.soup = None
        self.elements = None
        self.data = {}

    def get_url(self):
        self.url = input("Enter URL: ")
    
    def fetch_webpage_content(self):
        response = requests.get(self.url)
        self.html_content = response.text
    
    def initialize_beautifulsoup(self):
        self.soup = BeautifulSoup(self.html_content, 'html.parser')
    
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

    def extract_date(self):
        date_tag = self.soup.find('i', text=re.compile(r'\w+ \d{1,2}, \d{4}'))
        if date_tag:
            self.data['date'] = date_tag.get_text(strip=True)

    def extract_data_using_beautifulsoup(self):
        for key, regex_pattern in self.elements.items():
            # Find <th> tag containing the text with regex pattern
            th_tag = self.soup.find('th', text=re.compile(regex_pattern, re.IGNORECASE))
            if th_tag:
                # Find the corresponding <td> tag with the data
                td_tag = th_tag.find_next_sibling('td')
                if td_tag:
                    value = td_tag.get_text(strip=True)
                    # Clean up the value (remove commas)
                    value = value.replace(',', '')
                    self.data[key] = value
    
    def print_extracted_data(self):
        for key, value in self.data.items():
            print(f"{key}: {value}")

    def run(self):
        self.get_url()
        self.fetch_webpage_content()
        self.initialize_beautifulsoup()
        self.elements_for_search()
        self.suppress_deprecation_warning()
        self.extract_company_name()
        self.extract_date()
        self.extract_data_using_beautifulsoup()
        self.print_extracted_data()

if __name__ == '__main__':
    ExtractData = Scrap()
    ExtractData.run()