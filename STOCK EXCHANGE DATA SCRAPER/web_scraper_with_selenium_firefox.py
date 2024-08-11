from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import pandas as pd
from datetime import datetime

class Scrap:

    def __init__(self):
        self.options = Options()
        self.driver = None
        self.urls = []
        self.all_data = []
    
    def set_up_Firefox_options(self):
        self.options.add_argument('--headless')  # Run in headless mode for no GUI

    def create_a_new_instance_of_the_Firefox_driver(self):
        self.driver = webdriver.Firefox(options=self.options)

    def get_urls(self):
        self.urls = [
            'https://www.dsebd.org/displayCompany.php?name=LHBL',
            'https://www.dsebd.org/displayCompany.php?name=AMBEEPHA',
            'https://www.dsebd.org/displayCompany.php?name=BATBC',
        ]
    
    def elements_for_extraction(self):
        company_name = self.driver.find_element(By.XPATH, '//h2[contains(text(), "Company Name:")]/i').text
        date = self.driver.find_element(By.XPATH, '//h2[contains(text(), "Market Information:")]/i').text
        last_trading_price = self.driver.find_element(By.XPATH, '//th[contains(text(), "Last Trading Price")]/following-sibling::td').text
        opening_price = self.driver.find_element(By.XPATH, '//th[contains(text(), "Opening Price")]/following-sibling::td').text
        adjusted_opening_price = self.driver.find_element(By.XPATH, '//th[contains(text(), "Adjusted Opening Price")]/following-sibling::td').text
        yesterdays_closing_price = self.driver.find_element(By.XPATH, '//th[contains(text(), "Yesterday\'s Closing Price")]/following-sibling::td').text
        closing_price = self.driver.find_element(By.XPATH, '//th[contains(text(), "Closing Price")]/following-sibling::td').text
        days_range = self.driver.find_element(By.XPATH, '//th[contains(text(), "Day\'s Range")]/following-sibling::td').text
        weeks_52_moving_range = self.driver.find_element(By.XPATH, '//th[contains(text(), "52 Weeks\' Moving Range")]/following-sibling::td').text
        days_volume = self.driver.find_element(By.XPATH, '//th[contains(text(), "Day\'s Volume (Nos.)")]/following-sibling::td').text
        days_trade = self.driver.find_element(By.XPATH, '//th[contains(text(), "Day\'s Trade (Nos.)")]/following-sibling::td').text
        market_capitalization = self.driver.find_element(By.XPATH, '//th[contains(text(), "Market Capitalization (mn)")]/following-sibling::td').text

        self.data = {
                "Company Name": company_name,
                "Date": date,
                "Last Trading Price": last_trading_price,
                "Opening Price": opening_price,
                "Adjusted Opening Price": adjusted_opening_price,
                "Yesterday's Closing Price": yesterdays_closing_price,
                "Closing Price": closing_price,
                "Day's Range": days_range,
                "52 Weeks' Moving Range": weeks_52_moving_range,
                "Day's Volume": days_volume,
                "Day's Trade": days_trade,
                "Market Capitalization": market_capitalization,
        }

    def extract_data_from_each_URL_and_store(self):
        self.all_data = []
        for url in self.urls:
            self.driver.get(url)
            self.elements_for_extraction()
            self.all_data.append(self.data.copy())

    def print_the_extracted_data(self):
        for data in self.all_data:
            for key, value in data.items():
                print(f"  {key}: {value}")
            print("\n")

    def write_data_to_csv_file(self):
        df = pd.DataFrame(self.all_data)
        csv_file_name = f"extracted_data_{datetime.now().strftime('%Y-%m-%d')}.csv"
        df.to_csv(csv_file_name, index=False)
        print(f"Data has been written to {csv_file_name}")

    def close_the_browser(self):
        self.driver.quit()
    
    def run(self):
        self.set_up_Firefox_options()
        self.create_a_new_instance_of_the_Firefox_driver()
        self.get_urls()
        self.extract_data_from_each_URL_and_store()
        self.print_the_extracted_data()
        self.write_data_to_csv_file()
        self.close_the_browser()

if __name__ == '__main__':
    Scrap = Scrap()
    Scrap.run()