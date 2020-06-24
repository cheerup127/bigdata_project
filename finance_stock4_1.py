import bs4 as bs
import datetime as dt
import os
import pandas as pd
#from pandas.util.testing import assert_frame_equal
import pandas_datareader.data as web
import pickle
import requests

import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
#import pandas as pd
#import pandas_datareader.data as web

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.strip()
        tickers.append(ticker)
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers, f)
    print(tickers)
    return tickers
# save_sp500_tickers()

def save_medi_tickers():
    # tickers = ['NASDAQ:AMGN', 'NASDAQ:ADPT', 'NASDAQ:ALT', 'NASDAQ:PFE', 'NASDAQ:BNTX', \
    #  'NASDAQ:CYDY', 'NASDAQ:GILD', 'NASDAQ:GSK', 'NASDAQ:HTBX', 'NASDAQ:INO',\
    #       'NASDAQ:JNJ', 'NASDAQ:MRNA', 'NASDAQ:NVAX', 'NASDAQ:REGN']

    tickers = ['AMGN', 'ADPT', 'ALT', 'PFE', 'BNTX', 'CYDY', \
            'GILD', 'GSK', 'HTBX', 'INO', 'JNJ', 'MRNA', 'NVAX', 'REGN']
    with open("medicine_company.pickle","wb") as f:
        pickle.dump(tickers, f)
    print(tickers)
    return tickers

def get_data_from_yahoo(reload_sp500=False):
    
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle","rb") as f:
            tickers = pickle.load(f)
        
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2000,1,1)
    end = dt.datetime(2016,12,31)

    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            try:
                df = web.DataReader(ticker, 'yahoo', start, end)
                df.to_csv('stock_dfs/{}.csv'.format(ticker))
            except Exception as ex:
                print('Error:', ex)
        else:
            print('Already have {}'.format(ticker))

# get_data_from_yahoo(True)

def get_data_from_yahoo2(reload_medicom=False):
    if reload_medicom:
        tickers = save_medi_tickers()
    else:
        with open("medicine_company.pickle","rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs_covid19'):
        os.makedirs('stock_dfs_covid19')

    date_object = dt.date.today()
    start = dt.datetime(2019,1,1)
    end = dt.datetime(date_object.year,date_object.month,date_object.day)

    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stock_dfs_covid19/{}.csv'.format(ticker)):
            try:
                df = web.DataReader(ticker, 'yahoo', start, end)
                df.to_csv('stock_dfs_covid19/{}.csv'.format(ticker))
            except Exception as ex:
                print('Error:', ex)
        else:
            print('Already have {}'.format(ticker))
    
# get_data_from_google(True)


def show_csv_ggplot():
    style.use('ggplot')
    ## AMGN
    df = pd.read_csv('stock_dfs_covid19/AMGN.csv', parse_dates=True, index_col=0)#.to_datetime()
    # df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()  # moving average ??
    df_ohlc = df['Adj Close'].resample('10D').ohlc()
    df_volume = df['Volume'].resample('10D').sum()

    df_ohlc.reset_index(inplace=True)
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

    # df_ohlc_hv = df['Adj Close'].resample('10D').RANKVAL(d0, s0)
    print('AMGN: {}'.format(df_volume.max()))
### ax1.annotate('text', (date[11],highp[11]), xytext=(0.8, 0.9), textcoords='axes fraction',\
# arrowprops = dict(facecolor='gray',color='grey'))
  ###  ax1.text(df_ohlc, df_volume, 'ddd')

    ## ADPT
    df1 = pd.read_csv('stock_dfs_covid19/ADPT.csv', parse_dates=True, index_col=0)#.to_datetime()
    # df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()  # moving average ??
    df1_ohlc = df1['Adj Close'].resample('10D').ohlc()
    df1_volume = df1['Volume'].resample('10D').sum()

    df1_ohlc.reset_index(inplace=True)
    df1_ohlc['Date'] = df1_ohlc['Date'].map(mdates.date2num)

    print('ADPT: {}'.format(df1_volume.max()))

    ## ALT
    df2 = pd.read_csv('stock_dfs_covid19/ALT.csv', parse_dates=True, index_col=0)#.to_datetime()
    # df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()  # moving average ??
    df2_ohlc = df2['Adj Close'].resample('10D').ohlc()
    df2_volume = df2['Volume'].resample('10D').sum()

    df2_ohlc.reset_index(inplace=True)
    df2_ohlc['Date'] = df2_ohlc['Date'].map(mdates.date2num)

    print('ALT: {}'.format(df2_volume.max()))

    ## PFE
    df3 = pd.read_csv('stock_dfs_covid19/PFE.csv', parse_dates=True, index_col=0)#.to_datetime()
    # df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()  # moving average ??
    df3_ohlc = df3['Adj Close'].resample('10D').ohlc()
    df3_volume = df3['Volume'].resample('10D').sum()

    df3_ohlc.reset_index(inplace=True)
    df3_ohlc['Date'] = df3_ohlc['Date'].map(mdates.date2num)
    print('PFE: {}'.format(df3_volume.max()))

    ## BNTX
    df4 = pd.read_csv('stock_dfs_covid19/BNTX.csv', parse_dates=True, index_col=0)#.to_datetime()
    # df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()  # moving average ??
    df4_ohlc = df4['Adj Close'].resample('10D').ohlc()
    df4_volume = df4['Volume'].resample('10D').sum()

    df4_ohlc.reset_index(inplace=True)
    df4_ohlc['Date'] = df4_ohlc['Date'].map(mdates.date2num)
    print('BNTX: {}'.format(df4_volume.max()))

    ## CYDY
    df5 = pd.read_csv('stock_dfs_covid19/CYDY.csv', parse_dates=True, index_col=0)#.to_datetime()
    # df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()  # moving average ??
    df5_ohlc = df5['Adj Close'].resample('10D').ohlc()
    df5_volume = df5['Volume'].resample('10D').sum()

    df5_ohlc.reset_index(inplace=True)
    df5_ohlc['Date'] = df5_ohlc['Date'].map(mdates.date2num)
    print('CYDY: {}'.format(df5_volume.max()))

    ## GILD
    df6 = pd.read_csv('stock_dfs_covid19/GILD.csv', parse_dates=True, index_col=0)#.to_datetime()
    # df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()  # moving average ??
    df6_ohlc = df6['Adj Close'].resample('10D').ohlc()
    df6_volume = df6['Volume'].resample('10D').sum()

    df6_ohlc.reset_index(inplace=True)
    df6_ohlc['Date'] = df6_ohlc['Date'].map(mdates.date2num)
    print('GILD: {}'.format(df6_volume.max()))

    ## GSK
    df7 = pd.read_csv('stock_dfs_covid19/GSK.csv', parse_dates=True, index_col=0)#.to_datetime()
    # df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()  # moving average ??
    df7_ohlc = df7['Adj Close'].resample('10D').ohlc()
    df7_volume = df7['Volume'].resample('10D').sum()

    df7_ohlc.reset_index(inplace=True)
    df7_ohlc['Date'] = df7_ohlc['Date'].map(mdates.date2num)
    print('GSK: {}'.format(df7_volume.max()))

    ## HTBX
    df8 = pd.read_csv('stock_dfs_covid19/HTBX.csv', parse_dates=True, index_col=0)#.to_datetime()
    # df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()  # moving average ??
    df8_ohlc = df8['Adj Close'].resample('10D').ohlc()
    df8_volume = df8['Volume'].resample('10D').sum()

    df8_ohlc.reset_index(inplace=True)
    df8_ohlc['Date'] = df8_ohlc['Date'].map(mdates.date2num)
    print('HTBX: {}'.format(df8_volume.max()))

    ## INO
    df9 = pd.read_csv('stock_dfs_covid19/INO.csv', parse_dates=True, index_col=0)#.to_datetime()
    # df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()  # moving average ??
    df9_ohlc = df9['Adj Close'].resample('10D').ohlc()
    df9_volume = df9['Volume'].resample('10D').sum()

    df9_ohlc.reset_index(inplace=True)
    df9_ohlc['Date'] = df9_ohlc['Date'].map(mdates.date2num)
    print('INO: {}'.format(df9_volume.max()))

    ## JNJ
    df10 = pd.read_csv('stock_dfs_covid19/JNJ.csv', parse_dates=True, index_col=0)#.to_datetime()
    # df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()  # moving average ??
    df10_ohlc = df10['Adj Close'].resample('10D').ohlc()
    df10_volume = df10['Volume'].resample('10D').sum()

    df10_ohlc.reset_index(inplace=True)
    df10_ohlc['Date'] = df10_ohlc['Date'].map(mdates.date2num)
    print('JNJ: {}'.format(df10_volume.max()))

    ## MRNA
    df11 = pd.read_csv('stock_dfs_covid19/MRNA.csv', parse_dates=True, index_col=0)#.to_datetime()
    # df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()  # moving average ??
    df11_ohlc = df11['Adj Close'].resample('10D').ohlc()
    df11_volume = df11['Volume'].resample('10D').sum()

    df11_ohlc.reset_index(inplace=True)
    df11_ohlc['Date'] = df11_ohlc['Date'].map(mdates.date2num)
    print('MRNA: {}'.format(df11_volume.max()))

    ## NVAX
    df12 = pd.read_csv('stock_dfs_covid19/NVAX.csv', parse_dates=True, index_col=0)#.to_datetime()
    # df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()  # moving average ??
    df12_ohlc = df12['Adj Close'].resample('10D').ohlc()
    df12_volume = df12['Volume'].resample('10D').sum()

    df12_ohlc.reset_index(inplace=True)
    df12_ohlc['Date'] = df12_ohlc['Date'].map(mdates.date2num)
    print('NVAX: {}'.format(df12_volume.max()))

    ## REGN
    df13 = pd.read_csv('stock_dfs_covid19/REGN.csv', parse_dates=True, index_col=0)#.to_datetime()
    # df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()  # moving average ??
    df13_ohlc = df13['Adj Close'].resample('10D').ohlc()
    df13_volume = df13['Volume'].resample('10D').sum()

    df13_ohlc.reset_index(inplace=True)
    df13_ohlc['Date'] = df13_ohlc['Date'].map(mdates.date2num)
    print('REGN: {}'.format(df13_volume.max()))

# common 
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1) # 6 rows 1 cols
    ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
    ax1.xaxis_date() 

# df
    candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

# df1
    candlestick_ohlc(ax1, df1_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df1_volume.index.map(mdates.date2num), df1_volume.values, 0)

# df2
    candlestick_ohlc(ax1, df2_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df2_volume.index.map(mdates.date2num), df2_volume.values, 0)

# df3
    candlestick_ohlc(ax1, df3_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df3_volume.index.map(mdates.date2num), df3_volume.values, 0)

# df4
    candlestick_ohlc(ax1, df4_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df4_volume.index.map(mdates.date2num), df4_volume.values, 0)

# df5
    candlestick_ohlc(ax1, df5_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df5_volume.index.map(mdates.date2num), df5_volume.values, 0)

# df6
    candlestick_ohlc(ax1, df6_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df6_volume.index.map(mdates.date2num), df6_volume.values, 0)

# df7
    candlestick_ohlc(ax1, df7_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df7_volume.index.map(mdates.date2num), df7_volume.values, 0)

# df8
    candlestick_ohlc(ax1, df8_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df8_volume.index.map(mdates.date2num), df8_volume.values, 0)

# df9
    candlestick_ohlc(ax1, df9_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df9_volume.index.map(mdates.date2num), df9_volume.values, 0)

# df10
    candlestick_ohlc(ax1, df10_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df10_volume.index.map(mdates.date2num), df10_volume.values, 0)

# df11
    candlestick_ohlc(ax1, df11_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df11_volume.index.map(mdates.date2num), df11_volume.values, 0)

# df12
    candlestick_ohlc(ax1, df12_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df12_volume.index.map(mdates.date2num), df12_volume.values, 0)

# df13
    candlestick_ohlc(ax1, df13_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df13_volume.index.map(mdates.date2num), df13_volume.values, 0)
    # plt.show()


    ax1.annotate

def file_clean():
    cmd = 'cd /Users/admin/Documents/vs/stock_dfs_covid19 | rm *.csv'
    os.system(cmd)


file_clean()
get_data_from_yahoo2(True)
show_csv_ggplot()
plt.show()