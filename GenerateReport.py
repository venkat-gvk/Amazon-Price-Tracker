import json
from datetime import datetime


class GenerateReport:
    def __init__(self, search_name, url, products):
        print('Generating Report...')
        self.products = products
        self.search_name = search_name
        self.url = url
        date_time = GenerateReport.getDateAndTime()

        report = {
            'Report generated at': date_time,
            'website': self.url,
            'search_term': self.search_name,
            'currency': 'Rs',
            'price_range': 'Low to High',
            'No_of_items': len(self.products),
            'products': self.products,
        }

        file = open(f"{self.search_name}.json", 'w', encoding='utf-8')
        json.dump(report, file)
        file.close()
        print('Report Generated')
        print('Finished')

    @staticmethod
    def getDateAndTime():
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        return date_time
