from dataclasses import dataclass

import pytest

from .fallback_dict import FallbackDict


@dataclass
class FallbackTestCase:
    default_values: dict
    custom_values: dict
    result_values: dict


@dataclass
class FallbackDeepTestCase:
    default_values: dict
    custom_values: dict
    keys: tuple
    value: str


@dataclass
class FallbackErrorTestCase:
    default_values: dict
    custom_values: dict
    keys: tuple


FALLBACK_SIMPLE_TEST_CASES = [
    FallbackTestCase(
        {"Country": "UK"}, {"City": "London"}, {"Country": "UK", "City": "London"}
    ),
    FallbackTestCase({"Country": "Haiti"}, {}, {"Country": "Haiti"}),
    FallbackTestCase(
        {}, {"City": "Port Vila", "Year": 2001}, {"City": "Port Vila", "Year": 2001}
    ),
]


@pytest.mark.parametrize("case", FALLBACK_SIMPLE_TEST_CASES)
def test_simple_fallback_dict(case):
    answer = FallbackDict(case.default_values, case.custom_values)
    for key, value in case.result_values.items():
        assert answer[key] == value
    assert len(answer) == len(case.result_values)


FALLBACK_CUSTOM_CASES = [
    FallbackTestCase(
        {"Country": "UK", "City": "Unknown", "Year": "Unknown"},
        {"City": "London", "Year": 2021},
        {"Country": "UK", "City": "London", "Year": 2021},
    ),
    FallbackTestCase(
        {"Country": "UK", "City": "Unknown", "Year": "Unknown"},
        {
            "City": "London",
        },
        {"Country": "UK", "City": "London", "Year": "Unknown"},
    ),
    FallbackTestCase(
        {"Country": "Unknown", "City": "Unknown", "Year": "Unknown"},
        {"Country": "UK", "City": "London", "Year": 2021, "Population": "8.982"},
        {"Country": "UK", "City": "London", "Year": 2021, "Population": "8.982"},
    ),
    FallbackTestCase(
        {
            "Country": "UK",
            "City": "London",
            "Year": 2021,
        },
        {"Name": "Bob", "Experience": "5 years"},
        {
            "Country": "UK",
            "City": "London",
            "Year": 2021,
            "Name": "Bob",
            "Experience": "5 years",
        },
    ),
]


@pytest.mark.parametrize("case", FALLBACK_CUSTOM_CASES)
def test_custom_fallback_dict(case):
    answer = FallbackDict(case.default_values, case.custom_values)
    for key, value in case.result_values.items():
        assert answer[key] == value
    assert len(answer) == len(case.result_values)


FALLBACK_DEEP_INCLUSION_SIMPLE_CASES = [
    FallbackDeepTestCase(
        {"Moscow": {"South": {"Population": "Unknown"}}},
        {"Moscow": {"South": {"Population": "1.59"}}},
        ("Moscow", "South", "Population"),
        "1.59",
    ),
    FallbackDeepTestCase(
        {"Moscow": {"South": {"Brateevo": {"Square": "348"}}}},
        {"Moscow": {"South": {"Brateevo": {"Square": "763"}}}},
        ("Moscow", "South", "Brateevo", "Square"),
        "763",
    ),
]


@pytest.mark.parametrize("case", FALLBACK_DEEP_INCLUSION_SIMPLE_CASES)
def test_simple_deep_inclusion_fallback_dict(case):
    fallback_dict = FallbackDict(case.default_values, case.custom_values)
    answer_value = fallback_dict[case.keys[0]]
    for i in range(1, len(case.keys)):
        answer_value = answer_value[case.keys[i]]
    assert answer_value == case.value


DEEP_INCLUSION_DEFAULT_VALUES = {
    "Moscow": {
        "South": {
            "Population": "Unknown",
            "Brateevo": {"Square:": "763", "Population": "90000"},
        },
        "East": {"Population": "1.52", "Perovo": {"Square": "973"}},
    }
}

DEEP_INCLUSION_CUSTOM_VALUES = {
    "Moscow": {
        "South": {
            "Population": "1.59",
            "Brateevo": {"Population": "109000", "Density": "14381"},
            "Donskoy": {"Population": "51941"},
        }
    }
}

FALLBACK_DEEP_INCLUSION_CASES = [
    FallbackDeepTestCase(
        DEEP_INCLUSION_DEFAULT_VALUES,
        DEEP_INCLUSION_CUSTOM_VALUES,
        ("Moscow", "East", "Perovo", "Square"),
        "973",
    ),
    FallbackDeepTestCase(
        DEEP_INCLUSION_DEFAULT_VALUES,
        DEEP_INCLUSION_CUSTOM_VALUES,
        ("Moscow", "South", "Population"),
        "1.59",
    ),
    FallbackDeepTestCase(
        DEEP_INCLUSION_DEFAULT_VALUES,
        DEEP_INCLUSION_CUSTOM_VALUES,
        ("Moscow", "South", "Donskoy", "Population"),
        "51941",
    ),
    FallbackDeepTestCase(  # TODO: Fix an error associated with this test!
        DEEP_INCLUSION_DEFAULT_VALUES,
        DEEP_INCLUSION_CUSTOM_VALUES,
        ("Moscow", "South", "Brateevo", "Square"),
        "763",
    ),
    FallbackDeepTestCase(
        DEEP_INCLUSION_DEFAULT_VALUES,
        DEEP_INCLUSION_CUSTOM_VALUES,
        ("Moscow", "South", "Brateevo", "Density"),
        "14381",
    ),
    FallbackDeepTestCase(
        DEEP_INCLUSION_DEFAULT_VALUES,
        DEEP_INCLUSION_CUSTOM_VALUES,
        ("Moscow", "South", "Brateevo", "Population"),
        "109000",
    ),
]


@pytest.mark.parametrize("case", FALLBACK_DEEP_INCLUSION_CASES)
def test_deep_inclusion_fallback_dict(case):
    fallback_dict = FallbackDict(case.default_values, case.custom_values)
    answer_value = fallback_dict[case.keys[0]]
    for i in range(1, len(case.keys)):
        answer_value = answer_value[case.keys[i]]
    assert answer_value == case.value


FALLBACK_NO_VALUE_CASES = [
    FallbackErrorTestCase(
        {"Country": "UK", "City": "Unknown", "Year": "Unknown"},
        {"City": "London", "Year": 2021},
        ("Month",),
    ),
    FallbackErrorTestCase(
        {"Moscow": {"South": {"Brateevo": {"Square": "348"}}}},
        {"Moscow": {"South": {"Brateevo": {"Square": "763"}}}},
        ("Moscow", "East"),
    ),
    FallbackErrorTestCase(
        {"Moscow": {"South": {"Brateevo": {"Square": "348"}}}},
        {"Moscow": {"South": {"Brateevo": {"Square": "763"}}}},
        ("Moscow", "South", "Brateevo", "Population"),
    ),
    FallbackErrorTestCase(
        {"Moscow": {"South": {"Population": "Unknown"}}},
        {"Moscow": {"South": {"Population": "1.59"}}},
        ("London",),
    ),
    FallbackErrorTestCase(
        {"Moscow": {"South": {"Brateevo": None}}},
        {},
        ("Moscow", "South", "Brateevo", "Square"),
    ),
    FallbackErrorTestCase(
        {"Moscow": {"Population": "11.92"}}, {}, ("Moscow", "Population", "History")
    ),
]


@pytest.mark.parametrize("case", FALLBACK_NO_VALUE_CASES)
def test_no_value_fallback_dict(case):
    fallback_dict = FallbackDict(case.default_values, case.custom_values)
    try:
        answer_value = fallback_dict[case.keys[0]]
        for i in range(1, len(case.keys)):
            answer_value = answer_value[case.keys[i]]
    except KeyError:
        pass
    except TypeError:
        pass
