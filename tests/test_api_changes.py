
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
    result = client.query_imbalance_prices(country_code, start=start, end=end)
    result
