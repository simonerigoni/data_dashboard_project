# Quandl
#
# python -m src.connectors.quandl


import quandl
import pandas as pd


class QuandlConnector:
    def __init__(self, api_key: str):
        """Initialize the Quandl connector.

        Args:
            api_key (str): API token for authentication
        """
        self.api_key = api_key
        quandl.ApiConfig.api_key = self.api_key

    def get(self, ticker, start_date, end_date) -> pd.DataFrame:
        """Get.

        Args:

        Returns:
            pd.DataFrame: data
        """
        return pd.DataFrame(
            quandl.get("WIKI/" + ticker, start_date=start_date, end_date=end_date)
        )

    def get_table(self, ticker, qopts) -> pd.DataFrame:
        """Get table.

        Args:

        Returns:
            pd.DataFrame: data
        """
        return quandl.get_table("ZACKS/FC", paginate=False, ticker=ticker, qopts=qopts)


if __name__ == "__main__":
    from src.config import QUANDL_API_KEY

    print("Quandl")
    quandl_connector = QuandlConnector(QUANDL_API_KEY)

    print(quandl_connector.get("AAPL", "2018-01-01", "2018-01-31"))
    # print(quandl_connector.get_table('AAPL'))
else:
    pass
