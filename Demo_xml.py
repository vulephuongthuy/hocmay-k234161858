#Reading the data inside the xml file to a variable under the name data
from bs4 import BeautifulSoup

with open('../dataset/SalesTransactions.xml', 'r') as f:
    data = f.read()
#Passing the stored data inside the beautifulsoup parser
bs_data = BeautifulSoup(data, 'xml')

#Finding all instances of tag
UelSample = bs_data.find_all('UelSample')
print(UelSample)