import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# Fetch AMD stock data
amd = yf.Ticker("AMD")
country = amd.info.get('country')
sector = amd.info.get('sector')

amd_data = amd.history(period="max")
print(f"Country: {country}, Sector: {sector}")
print(amd_data.head(1))

# Fetch and parse Amazon stock data from a static webpage
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/amazon_data_webpage.html"
response = requests.get(url)
html_data = response.text

soup = BeautifulSoup(html_data, 'html.parser')

amazon_data = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"])
data = []

for row in soup.find("tbody").find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    open_price = col[1].text
    high = col[2].text
    low = col[3].text
    close = col[4].text
    adj_close = col[5].text
    volume = col[6].text

    data.append([date, open_price, high, low, close, adj_close, volume])

amazon_data = pd.DataFrame(data, columns=["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"])
print(amazon_data.head())

# Plotting AMD stock data
plt.figure(figsize=(10, 5))
plt.plot(amd_data.index, amd_data['Close'], label='AMD Close Price')
plt.title('AMD Stock Price Over Time')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.show()

# Plotting Amazon stock data
amazon_data['Date'] = pd.to_datetime(amazon_data['Date'])
amazon_data['Close'] = pd.to_numeric(amazon_data['Close'].str.replace(',', ''), errors='coerce')

plt.figure(figsize=(10, 5))
plt.plot(amazon_data['Date'], amazon_data['Close'], label='Amazon Close Price')
plt.title('Amazon Stock Price Over Time')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.show()
