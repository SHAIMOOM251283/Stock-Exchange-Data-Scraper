import re
import requests

class Scrap:

    def __init__(self):
        self.url = None
        self.html_content = None
        self.pattern = None
        self.matches = None

    def get_url(self):
        self.url = input("Enter URL: ")

    def fetch_webpage_content(self):
        response = requests.get(self.url)
        self.html_content = response.text
    
    def delineate_pattern(self):
        self.pattern = r'<td[^>]*>([\d., -]+)</td>'
    
    def find_matches(self):
        self.matches = re.findall(self.pattern, self.html_content)

    def extract(self):
        for match in self.matches:
            number = match.replace(',', '').strip()
            print(number)
    
    def run(self):
        self.get_url()
        self.fetch_webpage_content()
        self.delineate_pattern()
        self.find_matches()
        self.extract()
    
if __name__ == '__main__':
    Extract = Scrap()
    Extract.run()
