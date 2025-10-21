import os

from dotenv import load_dotenv
import pytest
from entsoe import EntsoePandasClient
import pandas as pd

load_dotenv()

API_KEY = str(os.getenv("API_KEY"))

import pandas as pd


@pytest.fixture
def client():
    yield EntsoePandasClient(api_key=API_KEY)


def test_sdac_mtu15_germany(client):
    country_code="DE"
    tz = "Europe/Berlin"
    start = pd.Timestamp("2025-10-10", tz=tz)
    end = pd.Timestamp("2025-10-11", tz=tz)
    # resolution = "60min"
    resolution = "15min"
    result = client.query_day_ahead_prices(
        country_code, start=start, end=end, resolution=resolution
    ).to_frame()
    result.index.name = "timestamp"
    missingp = pd.Timestamp("2024-12-31T00:00:00+01:00", tz="Europe/Brussels")
    begin = pd.Timestamp("2024-12-30T22:00:00+01:00", tz="Europe/Brussels")
    end = pd.Timestamp("2024-12-31T02:00:00+01:00", tz="Europe/Brussels")
    result.index = result.index.map(lambda x: x.isoformat())
    assert missingp in result.index


def test_sdac_mtu15_austria(client):
    country_code="AT"
    tz = "Europe/Vienna"
    start = pd.Timestamp("2025-10-11", tz=tz)
    end = pd.Timestamp("2025-10-12", tz=tz)
    # resolution = "60min"
    resolution = "15min"
    result = client.query_day_ahead_prices(
        country_code, start=start, end=end, resolution=resolution
    ).to_frame()
    result.index.name = "timestamp"
    missingp = pd.Timestamp("2024-12-31T00:00:00+01:00", tz="Europe/Brussels")
    begin = pd.Timestamp("2024-12-30T22:00:00+01:00", tz="Europe/Brussels")
    end = pd.Timestamp("2024-12-31T02:00:00+01:00", tz="Europe/Brussels")
    result.index = result.index.map(lambda x: x.isoformat())
    assert missingp in result.index


def test_sdac_mtu15_germany_lu(client):
    country_code="DE_LU"
    tz = "Europe/Berlin"
    start = pd.Timestamp("2025-10-10", tz=tz)
    end = pd.Timestamp("2025-10-11", tz=tz)
    # resolution = "60min"
    resolution = "15min"
    result = client.query_day_ahead_prices(
        country_code, start=start, end=end, resolution=resolution
    ).to_frame()
    result.index.name = "timestamp"
    missingp = pd.Timestamp("2024-12-31T00:00:00+01:00", tz="Europe/Brussels")
    begin = pd.Timestamp("2024-12-30T22:00:00+01:00", tz="Europe/Brussels")
    end = pd.Timestamp("2024-12-31T02:00:00+01:00", tz="Europe/Brussels")
    result.index = result.index.map(lambda x: x.isoformat())
    assert missingp in result.index


def test_imbalance_regression_457(client):
    """https://github.com/EnergieID/entsoe-py/issues/457"""
    country_code="AT"
    tz = "Europe/Vienna"
    start = pd.Timestamp("2025-10-20", tz=tz)
    end = pd.Timestamp("2025-10-21", tz=tz)
    client.query_imbalance_prices(country_code, start=start, end=end)


def test_dayahead_regression_445(client):
    """https://github.com/EnergieID/entsoe-py/issues/445"""
    country_code = "AT"
    tz = "Europe/Vienna"
    start = pd.Timestamp("2025-10-20", tz=tz)
    end = pd.Timestamp("2025-10-21", tz=tz)
    client.query_day_ahead_prices(country_code, start=start, end=end)


def test_issue_478():
    country_code = "DE"
    client = EntsoePandasClient(api_key=API_KEY)
    tz = "Europe/Vienna"
    start = pd.Timestamp("2025-11-10T00:00:00", tz=tz)
    end = pd.Timestamp("2026-12-01T00:00:00", tz=tz)
    df = client.query_imbalance_prices(country_code, start=start, end=end)
    assert df.shape[0] == 6369


def test_issue_482():
    country_code = "DE"
    client = EntsoePandasClient(api_key=API_KEY)
    tz = "Europe/Vienna"
    start = pd.Timestamp("2025-12-01T00:00:00", tz=tz)
    end = pd.Timestamp("2026-01-01T00:00:00", tz=tz)
    df = client.query_wind_and_solar_forecast(country_code, start=start, end=end)
    assert df.shape[0] == 2976


def test_issue_482_france():
    country_code = "FR"
    client = EntsoePandasClient(api_key=API_KEY)
    tz = "Europe/Vienna"
    start = pd.Timestamp("2022-08-01T00:00:00", tz=tz)
    end = pd.Timestamp("2023-01-01T00:00:00", tz=tz)
    df = client.query_wind_and_solar_forecast(country_code, start=start, end=end)
    assert df.shape[0] == 2976


def test_issue_486():
    country_code = "BE"
    client = EntsoePandasClient(api_key=API_KEY)

    start = pd.Timestamp("2025-11-06", tz="Europe/Berlin")
    end   = pd.Timestamp("2025-11-07", tz="Europe/Berlin")

    client.query_generation(country_code, start=start, end=end)


def test_issue_495():
    start = pd.Timestamp.today(tz="UTC").normalize() - pd.Timedelta(days=50)
    end = pd.Timestamp.today(tz="UTC").normalize()
    bidding_zone = "DE_AT_LU"
    client = EntsoePandasClient(api_key=API_KEY)

    response = client.query_unavailability_of_generation_units(
        country_code=bidding_zone,
        start=start,
        end=end,
    )


def test_issue_496():
    start = pd.Timestamp("20200101", tz="Europe/Brussels")
    # end = pd.Timestamp("20201201", tz="Europe/Brussels")
    end = pd.Timestamp("20230101", tz="Europe/Brussels")
    country_code = "NL"
    df = EntsoePandasClient(
        api_key=API_KEY
    ).query_installed_generation_capacity(
        country_code=country_code,
        # 'DE',
        start=start,
        end=end,
        psr_type=None,
    )
    df
