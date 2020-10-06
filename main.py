import urllib.request, re
from bs4 import BeautifulSoup
import csv, os.path
import datetime, os
import pandas as pd
import platform

# 코스피 최종 종목 파싱 리스트
stock_list0 = []

# 코스닥 최종 종목 파싱 리스트
stock_list = []


# 날짜
now = datetime.datetime.now()


# 코스닥 주소
url0 = 'https://finance.naver.com/sise/sise_quant.nhn?sosok=0'
html0 = urllib.request.urlopen(url0).read()
soup0 = BeautifulSoup(html0.decode('euc-kr', 'replace'), 'html.parser')

# 코스피 주소
url = 'https://finance.naver.com/sise/sise_quant.nhn?sosok=1'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html.decode('euc-kr', 'replace'), 'html.parser')


# 코스피 거래량 1000만 이상 종목 파싱
number0 = soup0.find_all(class_='number')

stock_volume0 = []
for i in range(3, 1000, 10):
    if (len(number0[i].text) < 10):
        break
    stock_volume0.append(number0[i].text)

num_to_parse0 = len(stock_volume0)

# 코스닥 거래량 1000만 이상 종목 파싱
number = soup.find_all(class_='number')

stock_volume = []
for i in range(3, 1000, 10):
    if (len(number[i].text) < 10):
        break
    stock_volume.append(number[i].text)

num_to_parse = len(stock_volume)


# 코스피 목차, 날짜 세팅
item0 = ['종목명', '코드', '상세정보']
item0.append(now.strftime('%y.%m.%d'))

stock_list0.append(item0)

# 코스닥 목차, 날짜 세팅
item = ['종목명', '코드', '상세정보']
item.append(now.strftime('%y.%m.%d'))

stock_list.append(item)


# 코스피 주식명 등락률 파싱
stock_name0 = soup0.select('.tltle')
stock_fluctuate0 = soup0.select('.tah.p11')

# 코스닥 주식명, 등락률 파싱
stock_name = soup.select('.tltle')
stock_fluctuate = soup.select('.tah.p11')


# 코스피 주식명, 코드번호, 상세정보 url, 등락률, 거래량
for i in range(0, num_to_parse0):
    tmp0 = []
    tmp0.append(stock_name0[i].text)
    tmp0.append(re.findall("\d+", stock_name0[i].attrs['href'])[0])
    tmp0.append('https://finance.naver.com' + stock_name0[i].attrs['href'])
    tmp0.append(stock_fluctuate0[2 * i + 1].text.strip() + ' / ' + stock_volume0[i])
    stock_list0.append(tmp0)

# 코스닥 주식명, 코드번호, 상세정보 url, 등락률, 거래량
for i in range(0, num_to_parse):
    tmp = []
    tmp.append(stock_name[i].text)
    tmp.append(re.findall("\d+", stock_name[i].attrs['href'])[0])
    tmp.append('https://finance.naver.com' + stock_name[i].attrs['href'])
    tmp.append(stock_fluctuate[2 * i + 1].text.strip() + ' / ' + stock_volume[i])
    stock_list.append(tmp)


# 코스피 CSV 파일 생성
if(platform.system() == 'Darwin'):
    os.chdir('/Users/cocoret/PycharmProjects/volumechaser/Kospi')
else:
    os.chdir('C:/Users/jae34/PycharmProjects/volumechaser/Kospi')

f0 = open(now.strftime('%y.%m.%d') + '.csv', 'w', encoding='utf-8', newline='')
csvWriter0 = csv.writer(f0)

for i in stock_list0:
    csvWriter0.writerow(i)

f0.close()

if(platform.system() == 'Darwin'):
    os.chdir('/Users/cocoret/PycharmProjects/volumechaser')
else:
    os.chdir('C:/Users/jae34/PycharmProjects/volumechaser')

# 코스닥 CSV 파일 생성
if(platform.system() == 'Darwin'):
    os.chdir('/Users/cocoret/PycharmProjects/volumechaser/Kosdaq')
else:
    os.chdir('C:/Users/jae34/PycharmProjects/volumechaser/Kosdaq')

f = open(now.strftime('%y.%m.%d') + '.csv', 'w', encoding='utf-8', newline='')
csvWriter = csv.writer(f)

for i in stock_list:
    csvWriter.writerow(i)

f.close()

if(platform.system() == 'Darwin'):
    os.chdir('/Users/cocoret/PycharmProjects/volumechaser')
else:
    os.chdir('C:/Users/jae34/PycharmProjects/volumechaser')

# ----------------------------------------------------------------------#

# 코스피 개별 종목 거래량 5일 간 추적 후 csv파일에 추가
a0 = 0
for i in range(1, 5):
    now_tmp10 = now + datetime.timedelta(days=-(i + a0))
    if (now_tmp10.isoweekday() == 7):
        now_tmp10 = now_tmp10 + datetime.timedelta(days=-2)
        a = 2
    now_tmp0 = now_tmp10.strftime('%y.%m.%d')

    if (platform.system() == 'Darwin'):
        path0 = f'/Users/cocoret/PycharmProjects/volumechaser/Kospi/{now_tmp0}.csv'
    else:
        path0 = f'C:/Users/jae34/PycharmProjects/volumechaser/Kospi/{now_tmp0}.csv'

    if os.path.isfile(path0):
        if (platform.system() == 'Darwin'):
            csv_input0 = pd.read_csv(f'/Users/cocoret/PycharmProjects/volumechaser/Kospi/{now_tmp0}.csv',
                                    dtype={'코드': 'str'})
        else:
            csv_input0 = pd.read_csv(f'C:/Users/jae34/PycharmProjects/volumechaser/Kospi/{now_tmp0}.csv',
                                    dtype={'코드': 'str'})

        rate_quant_tmp0 = []
        for x in range(0, len(csv_input0['코드'])):
            tmp0 = csv_input0['코드'][x]
            if (len(tmp0) == 5):
                tmp0 = '0' + tmp0
            individual_url0 = f'https://finance.naver.com/item/sise.nhn?code={tmp0}'
            individual_html0 = urllib.request.urlopen(individual_url0).read()
            individual_soup0 = BeautifulSoup(individual_html0, 'html.parser')

            compare0 = round(int(individual_soup0.select_one('#_quant').text.replace(',', '')) / (
                int(csv_input0[now_tmp0][x].split()[2].replace(',', ''))) * 100)
            rate_quant_tmp0.append(individual_soup0.select_one('#_rate').text.strip()
                                  + ' / ' + individual_soup0.select_one('#_quant').text + '(' + str(compare0) + '%)')

        date0 = now.strftime('%y.%m.%d')
        csv_input0[date0] = rate_quant_tmp0

        if (platform.system() == 'Darwin'):
            csv_input0.to_csv(f'/Users/cocoret/PycharmProjects/volumechaser/Kospi/{now_tmp0}.csv', index=False)
        else:
            csv_input0.to_csv(f'C:/Users/jae34/PycharmProjects/volumechaser/Kospi/{now_tmp0}.csv', index=False)


# 코스닥 개별 종목 거래량 5일 간 추적 후 csv파일에 추가

a = 0
for i in range(1, 5):
    now_tmp1 = now + datetime.timedelta(days=-(i + a))
    if (now_tmp1.isoweekday() == 7):
        now_tmp1 = now_tmp1 + datetime.timedelta(days=-2)
        a = 2
    now_tmp = now_tmp1.strftime('%y.%m.%d')

    if (platform.system() == 'Darwin'):
        path = f'/Users/cocoret/PycharmProjects/volumechaser/Kosdaq/{now_tmp}.csv'
    else:
        path = f'C:/Users/jae34/PycharmProjects/volumechaser/Kosdaq/{now_tmp}.csv'

    if os.path.isfile(path):
        if (platform.system() == 'Darwin'):
            csv_input = pd.read_csv(f'/Users/cocoret/PycharmProjects/volumechaser/Kosdaq/{now_tmp}.csv',
                                    dtype={'코드': 'str'})
        else:
            csv_input = pd.read_csv(f'C:/Users/jae34/PycharmProjects/volumechaser/Kosdaq/{now_tmp}.csv',
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

        if (platform.system() == 'Darwin'):
            csv_input.to_csv(f'/Users/cocoret/PycharmProjects/volumechaser/Kosdaq/{now_tmp}.csv', index=False)
        else:
            csv_input.to_csv(f'C:/Users/jae34/PycharmProjects/volumechaser/Kosdaq/{now_tmp}.csv', index=False)



