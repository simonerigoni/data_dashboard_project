# Data dashboard dash application
#
# python dash_app.py

import dash
import dash_bootstrap_components as dbc
import colorlover as cl
import datetime as dt
import numpy as np
import pandas as pd


from src.config import (
    QUANDL_API_KEY,
    TICKER_FILENAME,
    INDICATOR_FILENAME,
    DEFAULT_WINDOW_SIZE_BOLLINGER_BANDS,
    DEFAULT_NUM_OF_STD_BOLLINGER_BANDS,
    DEFAULT_AVAILABLE_YEARS,
    DEFAULT_TICKERS,
    DEFAULT_INDICATORS,
)
from src.connectors.quandl import QuandlConnector

EXTERNAL_STYLESHEETS = [
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css",
    {
        "href": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css",
        "rel": "stylesheet",
        "integrity": "sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u",
        "crossorigin": "anonymous",
    },
]

colorscale = cl.scales["9"]["qual"]["Paired"]
time_dictionary = {"1W": 7, "1M": 30, "1Y": 365, "5Y": 1825}


def _create_app(ticker_filename=TICKER_FILENAME, indicator_filename=INDICATOR_FILENAME):
    """
    Creates dash application

    Args:
        ticker_filename (str): ticker filename. Default value TICKER_FILENAME
        indicator_filename (str):: indicator filename. Default value INDICATOR_FILENAME

    Returns:
        app (dash.Dash or DjangoDash): Dash or DjangoDash application
    """

    app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
    quandl_connector = QuandlConnector(QUANDL_API_KEY)

    df_ticker = pd.read_csv(ticker_filename)
    df_indicator = pd.read_csv(indicator_filename)
    # dt.datetime.now() quandl does not provide data updated
    data_end_time = dt.datetime.strptime("2018-03-27", "%Y-%m-%d")
    # data_start_time = data_end_time - dt.timedelta(days = 365)
    window_size_bollinger_bands = DEFAULT_WINDOW_SIZE_BOLLINGER_BANDS
    num_of_std_bollinger_bands = DEFAULT_NUM_OF_STD_BOLLINGER_BANDS
    list_year = np.arange(
        data_end_time.date().year,
        data_end_time.date().year - DEFAULT_AVAILABLE_YEARS,
        -1,
    )

    app.layout = dash.html.Div(
        [
            dbc.Nav(
                [
                    dash.html.Div(
                        [
                            dash.html.Div(
                                [
                                    dash.html.A(
                                        "Data dashboard",
                                        href="/",
                                        className="navbar-brand",
                                    )
                                ],
                                className="navbar-header",
                            ),
                            dash.html.Div(
                                [
                                    dash.html.Ul(
                                        [
                                            dash.html.Li(
                                                dash.html.A(
                                                    "Made with Udacity",
                                                    href="https://www.udacity.com/",
                                                )
                                            ),
                                            dash.html.Li(
                                                dash.html.A(
                                                    "Github",
                                                    href="https://github.com/simonerigoni/data_dashboard_project",
                                                )
                                            ),
                                        ],
                                        className="nav navbar-nav",
                                    )
                                ],
                                className="collapse navbar-collapse",
                            ),
                        ],
                        className="container",
                    )
                ],
                className="navbar navbar-inverse navbar-fixed-top",
            ),
            dash.html.Div(
                [
                    dash.html.Div(
                        [
                            dash.html.H1(
                                "Quandle Finance Explorer", className="text-center"
                            ),
                            dash.html.H4(
                                "Data available only to {}".format(data_end_time.date())
                            ),
                            dash.html.H3("Compare Stocks"),
                            dash.dcc.Dropdown(
                                id="dropdown-stock-tickers",
                                options=[
                                    {"label": s[0], "value": s[1]}
                                    for s in zip(
                                        df_ticker.Company_Name, df_ticker.Ticker
                                    )
                                ],
                                value=DEFAULT_TICKERS,
                                multi=True,
                            ),
                            dash.html.H3("Timescale"),
                            dash.dcc.RadioItems(
                                id="radioitems-timescale",
                                options=[
                                    {"label": t, "value": t} for t in time_dictionary
                                ],
                                value="1Y",
                            ),
                            dash.html.H3("Bollinger bands parameters"),
                            dash.dcc.Checklist(
                                id="checklist-enable-bollinger-bands",
                                options=[{"label": "Enable", "value": "enable"}],
                                value=["enable"],
                            ),
                            dash.html.H4("Window size"),
                            dash.dcc.Input(
                                id="input-window-size-bollinger-bands",
                                type="number",
                                value=window_size_bollinger_bands,
                            ),
                            dash.html.H4("Number of standard deviation"),
                            dash.dcc.Input(
                                id="input-num-of-std-bollinger-bands",
                                type="number",
                                value=num_of_std_bollinger_bands,
                            ),
                            dash.html.H3("Graphs"),
                            dash.html.Div(id="graphs"),
                            dash.html.H3("Indicators"),
                            dash.html.H4("Years"),
                            dash.dcc.Dropdown(
                                id="dropdown-years",
                                options=[
                                    {"label": year, "value": year} for year in list_year
                                ],
                                value=[
                                    str(data_end_time.date().year),
                                    str(data_end_time.date().year - 1),
                                ],
                                multi=True,
                            ),
                            dash.html.H4("Indicators"),
                            dash.dcc.Dropdown(
                                id="dropdown-indicators",
                                options=[
                                    {"label": s[0], "value": s[1]}
                                    for s in zip(
                                        df_indicator.Name, df_indicator.Column_Code
                                    )
                                ],
                                value=DEFAULT_INDICATORS,
                                multi=True,
                            ),
                            dash.html.Div(id="tables"),
                        ],
                        className="container",
                    )
                ],
                className="jumbotron",
            ),
        ],
        className="container",
    )

    @app.callback(
        dash.dependencies.Output("graphs", "children"),
        [
            dash.dependencies.Input("dropdown-stock-tickers", "value"),
            dash.dependencies.Input("radioitems-timescale", "value"),
            dash.dependencies.Input("checklist-enable-bollinger-bands", "value"),
            dash.dependencies.Input("input-window-size-bollinger-bands", "value"),
            dash.dependencies.Input("input-num-of-std-bollinger-bands", "value"),
        ],
    )
    def update_graph(
        stock_tickers,
        timescale,
        enable_bollinger_bands,
        window_size_bollinger_bands,
        num_of_std_bollinger_bands,
    ):
        """
        Update the graphs

        Args:
            stock_tickers (list): selected tickers
            timescale (list): selected timescale
            enable_bollinger_bands (str): enable or disable bollinger bands
            window_size_bollinger_bands (int): window size for bollinger bands
            num_of_std_bollinger_bands (int): number of standar deviation for bollinger bands

        Returns:
            graphs (list): list of graphs
        """
        data_start_time = (
            data_end_time - dt.timedelta(days=time_dictionary[timescale])
        ).date()
        enable_bollinger_bands = (
            True
            if len(enable_bollinger_bands) > 0 and enable_bollinger_bands[0] == "enable"
            else False
        )
        graphs = []

        for i, ticker in enumerate(stock_tickers):
            graphs.append(dash.html.H4(ticker))
            try:
                df = quandl_connector.get(ticker, data_start_time, data_end_time)
            except Exception:
                # graphs.append(dash.html.H3('Data is not available for {}'.format(ticker))#, className = {'marginTop': 20, 'marginBottom': 20}))
                graphs.append(dash.html.H5("Data is not available"))
                continue

            candlestick = {
                "x": df.index,
                "open": df["Open"],
                "high": df["High"],
                "low": df["Low"],
                "close": df["Close"],
                "type": "candlestick",
                "name": ticker,
                "legendgroup": ticker,
                "increasing": {"line": {"color": colorscale[0]}},
                "decreasing": {"line": {"color": colorscale[1]}},
            }

            if enable_bollinger_bands is True:
                bb_bands = bollinger_bands(
                    df.Close, window_size_bollinger_bands, num_of_std_bollinger_bands
                )

                bollinger_traces = [
                    {
                        "x": df.index,
                        "y": y,
                        "type": "scatter",
                        "mode": "lines",
                        "line": {
                            "width": 1,
                            "color": colorscale[(i * 2) % len(colorscale)],
                        },
                        "hoverinfo": "none",
                        "legendgroup": ticker,
                        "showlegend": True if i == 0 else False,
                        "name": "{} - bollinger bands".format(ticker),
                    }
                    for i, y in enumerate(bb_bands)
                ]

            # graphs.append(dash.html.H4(ticker))
            graphs.append(
                dash.dcc.Graph(
                    id=ticker,
                    figure={
                        "data": [candlestick] + bollinger_traces
                        if enable_bollinger_bands is True
                        else [candlestick],
                        "layout": {
                            "margin": {"b": 0, "r": 10, "l": 60, "t": 0},
                            "legend": {"x": 0},
                        },
                    },
                )
            )
        return graphs

    @app.callback(
        dash.dependencies.Output("tables", "children"),
        [
            dash.dependencies.Input("dropdown-stock-tickers", "value"),
            dash.dependencies.Input("dropdown-years", "value"),
            dash.dependencies.Input("dropdown-indicators", "value"),
        ],
    )
    def update_table(stock_tickers, years, indicators):
        """
        Update the tables

        Args:
            stock_tickers (list): selected tickers
            years (int): selected years
            indicators (list): selected indicators

        Returns:
            tables (list): list of tables
        """
        tables = []
        for i, ticker in enumerate(stock_tickers):
            tables.append(dash.html.H4(ticker))
            try:
                colonne = [
                    "m_ticker",
                    "per_end_date",
                    "per_type",
                    "per_cal_year",
                ] + indicators
                df = quandl_connector.get_table(ticker, {"columns": colonne})
                # cd ..print(df)
            except Exception:
                tables.append(dash.html.H5("Data is not available"))
                continue

            if df.empty is True:
                tables.append(dash.html.H5("Data is not available"))
                continue

            df = df[df["per_type"] == "A"]
            df = df[["per_cal_year"] + indicators]
            anni = df["per_cal_year"].to_list()
            # print(anni)
            df = df.set_index("per_cal_year")
            df = df.transpose()
            df = df.reset_index()
            df.columns = ["Indicator"] + [str(y) for y in anni]
            # print(df)
            tables.append(
                dash.dash_table.DataTable(
                    id=ticker,
                    columns=[{"name": column, "id": column} for column in df.columns],
                    data=df.to_dict("records"),
                )
            )
        return tables

    return app


def bollinger_bands(
    price,
    window_size=DEFAULT_WINDOW_SIZE_BOLLINGER_BANDS,
    num_of_std=DEFAULT_NUM_OF_STD_BOLLINGER_BANDS,
):
    """
    Compute bollinger bands

    Args:
        price (float): ticker price
        window_size (int): window size
        num_of_std (int): number of standar deviation

    Returns:
        rolling_mean (float): rolling mean value
        upper_band (float): upper band
        lower_band (float): lower band
    """
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std * num_of_std)
    lower_band = rolling_mean - (rolling_std * num_of_std)
    return rolling_mean, upper_band, lower_band


if __name__ == "__main__":
    app = _create_app()
    app.run(debug=True)
else:
    pass
