import lxml                         #this is not directly used, but indirectly needed for line 23
import pandas as pd
import requests as req              #library that will post XHR and retrieve HTML
from bs4 import BeautifulSoup       #library that will parse HTML response of the XHR

def get_symbol_html(code):          #function that retrieves and parses HTML
    url = "https://www.investing.com/instruments/HistoricalDataAjax"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/79.0.3945.130 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    data = {
        "curr_id": code,
        "st_date": start_date,
        "end_date": end_date,
        "action": "historical_data",
        "sort_col": "date",
        "sort_ord": "ASC"
    }
    resp = req.post(url, data=data, headers=headers)
    return BeautifulSoup(resp.text, 'lxml')

def get_data_frame_from_html(html): #function that extracts relevant data from the HTML
    all_rows = []
    table = html.body.find("table", attrs={"id": "curr_table"})
    headers = table.find_all("th")
    header_array = []
    for header in headers:
        header_array.append(header.text)

    rows = table.find("tbody").find_all('tr')
    for row in rows:
        row_array = []
        cells = row.find_all('td')
        for cell in cells:
            row_array.append(cell.text.replace(",", "").replace("%", "").replace("K", ""))
        all_rows.append(row_array)
    init_df = pd.DataFrame(all_rows)
    init_df.columns = header_array
    return init_df

def restructure_df(init_df):        #function that converts types and deals with indexing and renaming
    if "Date" in init_df:
        init_df["Date"] = pd.to_datetime(init_df["Date"])
        init_df.set_index("Date", inplace=True)
    if "Open" in init_df:
        init_df["Open"] = init_df["Open"].astype(float)
    if "High" in init_df:
        init_df["High"] = init_df["High"].astype(float)
    if "Low" in init_df:
        init_df["Low"] = init_df["Low"].astype(float)
    if "Volume" in init_df:
        init_df["Volume"] = init_df["Volume"].astype(float) * 1000
    if "Change %" in init_df:
        init_df["Change %"] = init_df["Change %"].astype(float) / 100
        init_df.rename(columns={"Change %": "Change"}, inplace=True)

def download_dfs(path, btc, xau):   #function that extracts data and places it into a merged DataFrame
    print("Data download started.")

    btc_html = get_symbol_html(btc)
    xau_html = get_symbol_html(xau)

    btc_df = get_data_frame_from_html(btc_html)
    xau_df = get_data_frame_from_html(xau_html)

    restructure_df(btc_df)
    restructure_df(xau_df)

    btc_df.to_csv(path + "btc.csv")
    xau_df.to_csv(path + "xau.csv")

    print("Data download completed.")


your_path = "C:/Users/user/Desktop/"
start_date = "03/06/2017"
end_date = "03/06/2020"
btc_code = "945629"
xau_code = "68"
download_dfs(your_path, btc_code, xau_code)
