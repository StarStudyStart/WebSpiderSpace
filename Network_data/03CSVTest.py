import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('https://en.wikipedia.org/wiki/Comparison_of_text_editors')
bsObj = BeautifulSoup(html,'html.parser')
table = bsObj.find_all('table',{'class':'wikitable'})[0]
rows = table.find_all('tr')

csvFile = open('./editors.csv','wt',newline='',encoding='utf-8')
try:
	writer = csv.writer(csvFile)
	for row in rows:  #外层循环读取每行
		csvRow = []
		for cell in row.find_all(['td','th']): #内层循环读取一行中的每一个单元格
			csvRow.append(cell.get_text())
		writer.writerow((csvRow))
finally:
	csvFile.close()
	
	
