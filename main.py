import urllib.request, re
from bs4 import BeautifulSoup
import csv, os.path
import datetime, os
import pandas as pd

# 최종 종목 파싱 리스트
stock_list = []

# 날짜
now = datetime.datetime.now()

url = 'https://finance.naver.com/sise/sise_quant.nhn?sosok=1'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

# 거래량 1000만 이상 종목 파싱
number = soup.find_all(class_='number')

stock_volume = []
for i in range(3, 1000, 10):
    if (len(number[i].text) < 10):
        break
    stock_volume.append(number[i].text)

num_to_parse = len(stock_volume)

# 목차, 날짜 세팅
item = ['종목명', '코드', '상세정보']
item.append(now.strftime('%y.%m.%d'))

stock_list.append(item)

# 주식명, 등락률 파싱
stock_name = soup.select('.tltle')
stock_fluctuate = soup.select('.tah.p11')

# 주식명, 코드번호, 상세정보 url, 등락률, 거래량
for i in range(0, num_to_parse):
    tmp = []
    tmp.append(stock_name[i].text)
    tmp.append(re.findall("\d+", stock_name[i].attrs['href'])[0])
    tmp.append('https://finance.naver.com' + stock_name[i].attrs['href'])
    tmp.append(stock_fluctuate[2 * i + 1].text.strip() + ' / ' + stock_volume[i])
    stock_list.append(tmp)

# CSV 파일 생성
os.chdir('D:/PycharmProjects/volumechaser/StockData')

f = open(now.strftime('%y.%m.%d') + '.csv', 'w', encoding='utf-8', newline='')
csvWriter = csv.writer(f)

for i in stock_list:
    csvWriter.writerow(i)

f.close()
os.chdir('D:/PycharmProjects/volumechaser')

# ----------------------------------------------------------------------#

# 개별 종목 거래량 5일 간 추적 후 csv파일에 추가
#D:\PycharmProjects\volumechaser\StockData\20.05.19.csv
#path = f'D:/PycharmProjects/volumechaser/StockData/{now_tmp}.csv'

a = 0
for i in range(1, 5):
    now_tmp1 = now + datetime.timedelta(days=-(i + a))
    if (now_tmp1.isoweekday() == 7):
        now_tmp1 = now_tmp1 + datetime.timedelta(days=-2)
        a = 2
    now_tmp = now_tmp1.strftime('%y.%m.%d')
    path = f'D:/PycharmProjects/volumechaser/StockData/{now_tmp}.csv'
    if os.path.isfile(path):
        csv_input = pd.read_csv(f'D:/PycharmProjects/volumechaser/StockData/{now_tmp}.csv',
                                dtype={'코드': 'str'})

        rate_quant_tmp = []
        for x in range(0, len(csv_input['코드'])):
            tmp = csv_input['코드'][x]
            if (len(tmp) == 5):
                tmp = '0' + tmp
            individual_url = f'https://finance.naver.com/item/sise.nhn?code={tmp}'
            individual_html = urllib.request.urlopen(individual_url).read()
            individual_soup = BeautifulSoup(individual_html, 'html.parser')

            compare = round(int(individual_soup.select_one('#_quant').text.replace(',', '')) / (
                int(csv_input[now_tmp][x].split()[2].replace(',', ''))) * 100)
            rate_quant_tmp.append(individual_soup.select_one('#_rate').text.strip()
                                  + ' / ' + individual_soup.select_one('#_quant').text + '(' + str(compare) + '%)')

        date = now.strftime('%y.%m.%d')
        csv_input[date] = rate_quant_tmp
        csv_input.to_csv(f'D:/PycharmProjects/volumechaser/StockData/{now_tmp}.csv', index=False)


