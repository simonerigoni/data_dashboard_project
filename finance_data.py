# Finance data
#
# python finance_data.py


import datetime as dt

from src.config import QUANDL_API_KEY
from src.connectors.quandl import QuandlConnector


if __name__ == "__main__":
    print("Finance data")
    quandl_connector = QuandlConnector(QUANDL_API_KEY)
    ticker = "AAPL"
    data_end_time = dt.datetime.strptime("2018-03-27", "%Y-%m-%d")
    data_start_time = data_end_time - dt.timedelta(days=365)
    print(quandl_connector.get(ticker, data_start_time, data_end_time))
# colonne = ['m_ticker', 'per_end_date',
#            'per_type', 'per_cal_year'] + indicators
# df = quandl_connector.get_table(ticker, {'columns': colonne})
else:
    pass
