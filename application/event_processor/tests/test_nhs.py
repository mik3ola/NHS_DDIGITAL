import pytest
from datetime import time, date

from .conftest import PHARMACY_STANDARD_EVENT
from ..nhs import NHSEntity, is_std_opening_json, is_spec_opening_json
from opening_times import OpenPeriod, SpecifiedOpeningTime, StandardOpeningTimes

test_attr_names = ("odscode", "website", "PublicPhone", "Phone", "Postcode")


def test__init__():
    # Arrange
    test_data = PHARMACY_STANDARD_EVENT
    # Act
    nhs_entity = NHSEntity(test_data)
    # Assert
    assert nhs_entity.odscode == test_data["ODSCode"]
    assert nhs_entity.org_name == test_data["OrganisationName"]
    assert nhs_entity.org_type_id == test_data["OrganisationTypeId"]
    assert nhs_entity.org_type == test_data["OrganisationType"]
    assert nhs_entity.org_sub_type == test_data["OrganisationSubType"]
    assert nhs_entity.org_status == test_data["OrganisationStatus"]
    assert nhs_entity.postcode == test_data["Postcode"]
    assert nhs_entity.address_lines == [
        test_data["Address1"],
        test_data["Address2"],
        test_data["Address3"],
        test_data["City"],
        test_data["County"],
    ]


def test_get_specified_opening_times():
    # Arrange
    nhs_entity = NHSEntity(
        {
            "OpeningTimes": [
                {
                    "Weekday": "",
                    "Times": "08:45-17:00",
                    "OffsetOpeningTime": 525,
                    "OffsetClosingTime": 1020,
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Nov 12 2021",
                    "IsOpen": True,
                },
                {
                    "Weekday": "",
                    "Times": "09:00-16:00",
                    "OffsetOpeningTime": 540,
                    "OffsetClosingTime": 980,
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Jan  6    2022",
                    "IsOpen": True,
                },
                {
                    "Weekday": "",
                    "Times": "09:00-16:00",
                    "OffsetOpeningTime": 540,
                    "OffsetClosingTime": 980,
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Apr  01   2023",
                    "IsOpen": True,
                },
                {
                    "Weekday": "Thursday",
                    "Times": "08:45-18:00",
                    "OffsetOpeningTime": 525,
                    "OffsetClosingTime": 1080,
                    "OpeningTimeType": "General",
                    "AdditionalOpeningDate": "",
                    "IsOpen": True,
                },
            ]
        }
    )
    # Act
    # Assert

    expected = [
        SpecifiedOpeningTime([OpenPeriod(time(8, 45, 0), time(17, 0, 0))], date(2021, 11, 12)),
        SpecifiedOpeningTime([OpenPeriod(time(9, 0, 0), time(16, 0, 0))], date(2022, 1, 6)),
        SpecifiedOpeningTime([OpenPeriod(time(9, 0, 0), time(16, 0, 0))], date(2023, 4, 1)),
    ]

    actual_spec_open_times = nhs_entity.specified_opening_times
    assert len(actual_spec_open_times) == len(
        expected
    ), f"Should return {len(expected)} , actually: {len(actual_spec_open_times)}"

    for exp_spec_open_time in expected:
        assert (
            exp_spec_open_time in actual_spec_open_times
        ), f"NHS entity should contain {exp_spec_open_time} but can't be found in list {actual_spec_open_times}"


def test_get_standard_opening_times():
    # Arrange
    nhs_entity = NHSEntity(
        {
            "OpeningTimes": [
                {
                    "Weekday": "Friday",
                    "Times": "08:45-17:00",
                    "OpeningTimeType": "General",
                    "AdditionalOpeningDate": "",
                    "IsOpen": True,
                },
                {
                    "Weekday": "",
                    "Times": "08:45-18:00",
                    "OpeningTimeType": "Additional",
                    "AdditionalOpeningDate": "Jan 23 2022",
                    "IsOpen": True,
                },
                {
                    "Weekday": "Thursday",
                    "Times": "09:00-17:00",
                    "OpeningTimeType": "General",
                    "AdditionalOpeningDate": "",
                    "IsOpen": True,
                },
                {
                    "Weekday": "Saturday",
                    "Times": "08:45-18:00",
                    "OpeningTimeType": "Invalid_Type",
                    "AdditionalOpeningDate": "",
                    "IsOpen": True,
                },
            ]
        }
    )
    # Act
    expected_std_open_times = StandardOpeningTimes()
    expected_std_open_times.friday.append(OpenPeriod(time(8, 45, 0), time(17, 0, 0)))
    expected_std_open_times.thursday.append(OpenPeriod(time(9, 0, 0), time(17, 0, 0)))

    actual_std_open_times = nhs_entity.standard_opening_times

    # Assert
    assert actual_std_open_times == expected_std_open_times, (
        f"Actual std openings differ from expected. Actual={actual_std_open_times} "
        f"and Expected: {expected_std_open_times}"
    )


@pytest.mark.parametrize("organisation_status", ["Visible", "OTHER"])
def test_is_status_hidden_or_closed_open_service(organisation_status: str):
    # Arrange
    test_data = {"OrganisationStatus": organisation_status}
    nhs_entity = NHSEntity(test_data)
    # Act
    result = nhs_entity.is_status_hidden_or_closed()
    # Assert
    assert not result


@pytest.mark.parametrize("organisation_status", NHSEntity.CLOSED_AND_HIDDEN_STATUSES)
def test_is_status_hidden_or_closed_not_open_service(organisation_status: str):
    # Arrange
    test_data = {"OrganisationStatus": organisation_status}
    nhs_entity = NHSEntity(test_data)
    # Act
    result = nhs_entity.is_status_hidden_or_closed()
    # Assert
    assert result


@pytest.mark.parametrize(
    "open_time_json, expected",
    [
        ({}, False),
        (
            {
                "Weekday": "Sunday",
                "Times": "10:00-17:00",
                "OffsetOpeningTime": 540,
                "OffsetClosingTime": 780,
                "OpeningTimeType": "General",
                "AdditionalOpeningDate": "",
                "IsOpen": True,
            },
            True,
        ),
        (
            {
                "Weekday": "Tuesday",
                "Times": "01:00-23:59",
                "OpeningTimeType": "General",
                "AdditionalOpeningDate": "",
                "IsOpen": True,
            },
            True,
        ),
        (
            {
                "Weekday": "Sunday",
                "Times": "10:00-17:00",
                "OpeningTimeType": "",
                "AdditionalOpeningDate": "",
                "IsOpen": True,
            },
            False,
        ),
        (
            {
                "Weekday": "blursday",
                "Times": "10:00-17:00",
                "OpeningTimeType": "General",
                "AdditionalOpeningDate": "",
                "IsOpen": True,
            },
            False,
        ),
        (
            {
                "Weekday": "Sunday",
                "Times": "08:00-24:00",
                "OpeningTimeType": "General",
                "AdditionalOpeningDate": "",
                "IsOpen": True,
            },
            False,
        ),
        (
            {
                "Weekday": "Sunday",
                "Times": "10:00-17:00",
                "OpeningTimeType": "Additional",
                "AdditionalOpeningDate": "",
                "IsOpen": True,
            },
            False,
        ),
        (
            {
                "Weekday": "Sunday",
                "Times": "10:00-17:00",
                "OpeningTimeType": "General",
                "AdditionalOpeningDate": "Apr 23 2012",
                "IsOpen": True,
            },
            False,
        ),
        (
            {
                "Weekday": "Wednesday",
                "Times": "09:00-17:00",
                "OpeningTimeType": "General",
                "AdditionalOpeningDate": "",
                "IsOpen": True,
            },
            True,
        ),
        (
            {
                "Weekday": "Wednesday",
                "Times": "10:00-17:00",
                "OpeningTimeType": "General",
                "AdditionalOpeningDate": "",
                "IsOpen": False,
            },
            False,
        ),
        (
            {
                "Weekday": "Wednesday",
                "Times": "",
                "OpeningTimeType": "General",
                "AdditionalOpeningDate": "",
                "IsOpen": False,
            },
            True,
        ),
        (
            {
                "Weekday": "Wednesday",
                "Times": "",
                "OpeningTimeType": "General",
                "AdditionalOpeningDate": "",
                "IsOpen": True,
            },
            False,
        ),
        (
            {
                "Weekday": "Sunday",
                "Times": "10:00-17:00",
                "OpeningTimeType": "General",
                "AdditionalOpeningDate": "",
            },
            False,
        ),
        ({"Weekday": "Sunday", "OpeningTimeType": "General", "AdditionalOpeningDate": "", "IsOpen": False}, True),
        (
            {
                "Weekday": "Sunday",
                "Times": None,
                "OpeningTimeType": "General",
                "AdditionalOpeningDate": "",
                "IsOpen": False,
            },
            True,
        ),
        (
            {
                "Weekday": "",
                "Times": "10:00-17:00",
                "OpeningTimeType": "Additional",
                "AdditionalOpeningDate": "Nov 23 2023",
                "IsOpen": True,
            },
            False,
        ),
    ],
)
def test_is_std_opening_json(open_time_json, expected):
    actual = is_std_opening_json(open_time_json)
    assert actual == expected, f"Std time should be valid={expected} but wasn't. open_time={open_time_json}"


@pytest.mark.parametrize(
    "open_time_json, expected",
    [
        ({}, False),
        (
            {
                "Weekday": "",
                "Times": "10:00-17:00",
                "OffsetOpeningTime": 540,
                "OffsetClosingTime": 780,
                "OpeningTimeType": "Additional",
                "AdditionalOpeningDate": "Apr 23 2021",
                "IsOpen": True,
            },
            True,
        ),
        (
            {
                "Weekday": "Sunday",
                "Times": "10:00-17:00",
                "OffsetOpeningTime": 540,
                "OffsetClosingTime": 780,
                "OpeningTimeType": "Additional",
                "AdditionalOpeningDate": "Apr 14 2021",
                "IsOpen": True,
            },
            True,
        ),
        (
            {
                "Weekday": "Sunday",
                "Times": "10:00-17:00",
                "OpeningTimeType": "Additional",
                "AdditionalOpeningDate": "Apr 32 2021",
                "IsOpen": True,
            },
            False,
        ),
        (
            {
                "Weekday": "",
                "Times": "10:00-25:00",
                "OpeningTimeType": "Additional",
                "AdditionalOpeningDate": "Apr 14 2021",
                "IsOpen": True,
            },
            False,
        ),
        (
            {
                "Weekday": "Sunday",
                "Times": "10:00-17:00",
                "OpeningTimeType": "Additional",
                "AdditionalOpeningDate": "Apr 14 2021",
                "IsOpen": True,
            },
            True,
        ),
        (
            {
                "Weekday": "",
                "Times": "10:00-17:00",
                "OpeningTimeType": "General",
                "AdditionalOpeningDate": "Apr 14 2021",
                "IsOpen": True,
            },
            False,
        ),
        (
            {
                "Weekday": "",
                "Times": "10:00-17:00",
                "OpeningTimeType": "General",
                "AdditionalOpeningDate": "Apr 14 2021",
                "IsOpen": True,
            },
            False,
        ),
        (
            {
                "Weekday": "",
                "Times": "",
                "OpeningTimeType": "Additional",
                "AdditionalOpeningDate": "Jan 1 2021",
                "IsOpen": False,
            },
            True,
        ),
        (
            {
                "Weekday": "",
                "Times": "12:00-13:00",
                "OpeningTimeType": "Additional",
                "AdditionalOpeningDate": "Jan 1 2021",
                "IsOpen": False,
            },
            False,
        ),
        (
            {
                "Weekday": "",
                "Times": "",
                "OpeningTimeType": "Additional",
                "AdditionalOpeningDate": "Jan 1 2021",
                "IsOpen": True,
            },
            False,
        ),
        (
            {
                "Weekday": "Sunday",
                "Times": "10:00-17:00",
                "OffsetOpeningTime": 540,
                "OffsetClosingTime": 780,
                "OpeningTimeType": "General",
                "AdditionalOpeningDate": "",
                "IsOpen": True,
            },
            False,
        ),
        (
            {
                "Weekday": "",
                "Times": "10:00-17:00",
                "OpeningTimeType": "Additional",
                "AdditionalOpeningDate": "Apr 23 20211",
                "IsOpen": True,
            },
            False,
        ),
        (
            {
                "Weekday": "",
                "Times": "10:00-17:00",
                "OpeningTimeType": "Additional",
                "AdditionalOpeningDate": "",
                "IsOpen": True,
            },
            False,
        ),
        ({"Weekday": "", "Times": "10:00-17:00", "OpeningTimeType": "Additional", "IsOpen": True}, False),
        ({"Weekday": "", "Times": "10:00-17:00", "AdditionalOpeningDate": "Jan 30 2033", "IsOpen": True}, False),
    ],
)
def test_is_spec_opening_json(open_time_json, expected):
    actual = is_spec_opening_json(open_time_json)
    assert actual == expected, f"Spec time should be valid={expected} but wasn't. open_time={open_time_json}"
