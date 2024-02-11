import requests
from enum import Enum
from constants import API_KEY, BASE_URL, TEMP_C, KEY, MIN_C, MAX_C, AVERAGE_C


class CalculationType(Enum):
    MIN = 0,
    MAX = 1,
    AVERAGE = 2


def create_value_dict(day_data: dict) -> dict[Enum, float]:
    """
    Gets values represents values and return dict with enum as key and given value as value
    :param day_data: data from request
    :return:
    dict[Enum, float]
    """
    min_value = day_data[MIN_C]
    max_value = day_data[MAX_C]
    average_value = day_data[AVERAGE_C]
    return {CalculationType.AVERAGE: average_value, CalculationType.MIN: min_value,
            CalculationType.MAX: max_value}


def execute_request(url: str, params: dict) -> dict:
    """
    Execute http GET request with specific url and parameters
    :param url: specific url to execute in addition to base url
    :param params: relevant parameters for request
    :return:
    Response in json format
    """
    params[KEY] = API_KEY
    response = requests.get(BASE_URL + url, params=params)
    assert response.status_code == 200
    return response.json()


def calculate_temp_value(temp_values: list, c_type: CalculationType, round_data: None | int = None) -> float:
    """
    Calculate Min/Max/Average value in list of values according to selected type
    :param temp_values: list on values to calculate
    :param c_type: type of calculation - Min/Max/Average
    :param round_data: rounds the data to given decimal numbers (None = No rounding)
    :return:
    Calculated value
    """
    ret_val = None
    match c_type:
        case CalculationType.MIN:
            ret_val = min([t[TEMP_C] for t in temp_values])
        case CalculationType.MAX:
            ret_val = max([t[TEMP_C] for t in temp_values])
        case CalculationType.AVERAGE:
            ret_val = sum([t[TEMP_C] for t in temp_values]) / len(temp_values)

    return ret_val if round_data is None else round(ret_val, round_data)

