from bs4 import BeautifulSoup
import requests
import xlrd


class YahooFinance(object):
    def __init__(self):
        self.stock = ''
        self.stock_arr = []

    def create(self):
        loc = 'ReadFile/listinexcel.xlsx'
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)

        f = open('list.txt', 'w')

        for i in range(1, sheet.nrows):
            company = []
            for j in range(2):
                company.append(sheet.cell_value(i, j))
            self.stock_arr.append(company)
        f.write(str(self.stock_arr))
        f.close()
        return self.stock_arr

    def ask_stock(self):
        run = True
        while run:
            val = input("Enter your stock: ").upper()
            for i in self.stock_arr:
                try:
                    if val in i:
                        self.stock = i
                        run = False
                except Exception as e:
                    print(e)
        return self.stock

    def search(self):
        link = str('https://finance.yahoo.com/quote/' + str(self.stock[0]) + '?p=' + str(self.stock[0]))
        print(link)
        result = requests.get(link)
        src = result.content
        soup = BeautifulSoup(src, "lxml")
        while True:
            try:
                table = soup.find('table', attrs={'class': 'W(100%)'})
                table_body = table.find('tbody')
                rows = table_body.find_all('tr')
                print(self.stock[1])
                for row in rows:
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    print(cols)
            except AttributeError:
                print('retrying....')
            else:
                break


run = True
while run:
    val = input("Would you like to search for stocks? (Yes, yes, Y, y): ").upper()
    if val == 'Yes' or val == 'yes' or val == 'y' or val == 'Y':
        stock_market = YahooFinance()
        stock_market.create()
        stock_market.ask_stock()
        stock_market.search()
    else:
        print('Dont be shy search again!!')
        run = False
