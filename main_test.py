import pytest
import logging
import datetime
from common_methods import CalculationType, calculate_temp_value, execute_request, create_value_dict
from constants import *

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope='class')
def relevant_date() -> str:
    """
    Fixture to create date string for specific 'days ago' as configured in constants
    :return:
    Relevant date in string format
    """
    return (datetime.datetime.now() - datetime.timedelta(days=DAYS_AGO)).strftime("%Y-%m-%d")


class TestWeather:

    @pytest.mark.parametrize("city", ["Paris"])
    def test_history_and_values_by_name(self, city, relevant_date):
        LOGGER.info(f'Checking history forecast for {DAYS_AGO} days ago ({relevant_date}) for city {city}')
        res = execute_request(HISTORY_URL,
                              {CITY_PARAM: city, DATE_PARAM: relevant_date})
        forecast_object = res[FORECAST][FORECASTDAY][0]
        assert forecast_object[DATE] == str(relevant_date)
        hourly_temp = forecast_object[HOUR]
        day_data = forecast_object[DAY]
        temp_values = create_value_dict(day_data)
        for calc_type, expected_value in temp_values.items():
            LOGGER.info(f'Validate {calc_type.name} = {expected_value}')
            assert calculate_temp_value(hourly_temp, CalculationType(calc_type), 1) == expected_value
        pytest.forecast_data_global = res  # save res as global variable in order to use in another test

    def test_sunrise_by_location(self, relevant_date):
        assert pytest.forecast_data_global is not None
        LOGGER.info(f'Comparing forecast sunrise time between city name and location results')
        lon = pytest.forecast_data_global[LOCATION][LON]
        lat = pytest.forecast_data_global[LOCATION][LAT]
        sunrise_time = pytest.forecast_data_global[FORECAST][FORECASTDAY][0][ASTRO][SUNRISE]
        res = execute_request(HISTORY_URL,
                              {CITY_PARAM: f'{lat},{lon}', DATE_PARAM: relevant_date})
        assert res[FORECAST][FORECASTDAY][0][ASTRO][SUNRISE] == sunrise_time

    @pytest.mark.parametrize("search_value,expected_values", [("sama", 5)])
    def test_search(self, search_value, expected_values):
        LOGGER.info(f'Validate search result for {search_value} contains {expected_values} elements')
        res = execute_request(SEARCH_URL,
                              {CITY_PARAM: search_value})
        assert len(res) == expected_values
