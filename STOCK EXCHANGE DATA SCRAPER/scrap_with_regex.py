import re
import requests

class Scrap:

    def __init__(self):
        self.url = input("Enter URL: ")
        response = requests.get(self.url)
        self.html_content = response.text
        pattern = r'<td[^>]*>([\d., -]+)</td>'
        self.matches = re.findall(pattern, self.html_content)

    def extract(self):
        for match in self.matches:
            number = match.replace(',', '').strip()
            print(number)

if __name__ == '__main__':
    Extract = Scrap()
    Extract.extract()
