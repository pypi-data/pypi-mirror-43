from data_worker.wrappers.wrapper import Wrapper, WrapperSingleton

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators


class AlphaVantageWrapper(Wrapper, metaclass=WrapperSingleton):

    # TODO: Add Quote Endpoint & Search Endpoint wrapper functions

    def __init__(self, name, alt_names, api_meta_data):
        super().__init__(name, alt_names)
        self.ts = TimeSeries(key=api_meta_data['key'], output_format='pandas', indexing_type='integer')
        self.ti = TechIndicators(key=api_meta_data['key'], output_format='pandas', indexing_type='integer')

    def get_prices(self, ticker, interval, mins=None, adjusted=False):
        assert interval in ['intraday', 'daily', 'weekly', 'monthly'], (
            "Interval must be 'intraday', 'daily', 'weekly', or 'monthly'"
        )

        if interval == 'intraday':
            assert mins in [1, 5, 15, 30, 60], (
                "Minute interval must be specified as 1, 5, 15, 30, or 60"
            )

            data, _ = self.ts.get_intraday(ticker, str(mins) + 'min', 'full')

        if interval == 'daily' and adjusted:
            data, _ = self.ts.get_daily_adjusted(ticker, 'full')
        if interval == 'daily' and not adjusted:
            data, _ = self.ts.get_daily(ticker, 'full')
        if interval == 'weekly' and adjusted:
            data, _ = self.ts.get_weekly_adjusted(ticker)
        if interval == 'weekly' and not adjusted:
            data, _ = self.ts.get_weekly(ticker)
        if interval == 'monthly' and adjusted:
            data, _ = self.ts.get_monthly_adjusted(ticker)
        if interval == 'monthly' and not adjusted:
            data, _ = self.ts.get_monthly(ticker)

        return data

    def get_technical_indicator(self):
        data, _ = self.ti.get_aroon('AAPL')

        return data
