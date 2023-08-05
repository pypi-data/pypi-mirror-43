# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class Me(Model):
    """Me.

    :param place:
    :type place: ~energycap.sdk.models.PlaceChild
    :param cost_center:
    :type cost_center: ~energycap.sdk.models.CostCenterChild
    :param token:
    :type token: str
    :param system_user_code:
    :type system_user_code: str
    :param system_user_id:
    :type system_user_id: int
    :param full_name:
    :type full_name: str
    :param email:
    :type email: str
    :param number_of_accounting_periods:
    :type number_of_accounting_periods: int
    :param calendarization_method:
    :type calendarization_method: str
    :param fiscal_year_start_month:
    :type fiscal_year_start_month: int
    :param fiscal_year_method:
    :type fiscal_year_method: str
    :param claim:
    :type claim: list[~energycap.sdk.models.Claim]
    :param preference:
    :type preference: ~energycap.sdk.models.Preference
    :param date_formats:
    :type date_formats: list[str]
    :param time_formats:
    :type time_formats: list[~energycap.sdk.models.TimeFormatResponse]
    :param currency_unit:
    :type currency_unit: ~energycap.sdk.models.UnitChild
    :param current_accounting_period:
    :type current_accounting_period: int
    :param user_role_name:
    :type user_role_name: str
    :param permissions:
    :type permissions: ~energycap.sdk.models.Permissions
    :param feature_flags:
    :type feature_flags: list[str]
    :param upgrade_version_v3:
    :type upgrade_version_v3: str
    :param upgrade_version_v7:
    :type upgrade_version_v7: str
    :param sku:
    :type sku: str
    :param environment:
    :type environment: str
    :param build_date:
    :type build_date: datetime
    """

    _attribute_map = {
        'place': {'key': 'place', 'type': 'PlaceChild'},
        'cost_center': {'key': 'costCenter', 'type': 'CostCenterChild'},
        'token': {'key': 'token', 'type': 'str'},
        'system_user_code': {'key': 'systemUserCode', 'type': 'str'},
        'system_user_id': {'key': 'systemUserId', 'type': 'int'},
        'full_name': {'key': 'fullName', 'type': 'str'},
        'email': {'key': 'email', 'type': 'str'},
        'number_of_accounting_periods': {'key': 'numberOfAccountingPeriods', 'type': 'int'},
        'calendarization_method': {'key': 'calendarizationMethod', 'type': 'str'},
        'fiscal_year_start_month': {'key': 'fiscalYearStartMonth', 'type': 'int'},
        'fiscal_year_method': {'key': 'fiscalYearMethod', 'type': 'str'},
        'claim': {'key': 'claim', 'type': '[Claim]'},
        'preference': {'key': 'preference', 'type': 'Preference'},
        'date_formats': {'key': 'dateFormats', 'type': '[str]'},
        'time_formats': {'key': 'timeFormats', 'type': '[TimeFormatResponse]'},
        'currency_unit': {'key': 'currencyUnit', 'type': 'UnitChild'},
        'current_accounting_period': {'key': 'currentAccountingPeriod', 'type': 'int'},
        'user_role_name': {'key': 'userRoleName', 'type': 'str'},
        'permissions': {'key': 'permissions', 'type': 'Permissions'},
        'feature_flags': {'key': 'featureFlags', 'type': '[str]'},
        'upgrade_version_v3': {'key': 'upgradeVersion_V3', 'type': 'str'},
        'upgrade_version_v7': {'key': 'upgradeVersion_V7', 'type': 'str'},
        'sku': {'key': 'sku', 'type': 'str'},
        'environment': {'key': 'environment', 'type': 'str'},
        'build_date': {'key': 'buildDate', 'type': 'iso-8601'},
    }

    def __init__(self, place=None, cost_center=None, token=None, system_user_code=None, system_user_id=None, full_name=None, email=None, number_of_accounting_periods=None, calendarization_method=None, fiscal_year_start_month=None, fiscal_year_method=None, claim=None, preference=None, date_formats=None, time_formats=None, currency_unit=None, current_accounting_period=None, user_role_name=None, permissions=None, feature_flags=None, upgrade_version_v3=None, upgrade_version_v7=None, sku=None, environment=None, build_date=None):
        super(Me, self).__init__()
        self.place = place
        self.cost_center = cost_center
        self.token = token
        self.system_user_code = system_user_code
        self.system_user_id = system_user_id
        self.full_name = full_name
        self.email = email
        self.number_of_accounting_periods = number_of_accounting_periods
        self.calendarization_method = calendarization_method
        self.fiscal_year_start_month = fiscal_year_start_month
        self.fiscal_year_method = fiscal_year_method
        self.claim = claim
        self.preference = preference
        self.date_formats = date_formats
        self.time_formats = time_formats
        self.currency_unit = currency_unit
        self.current_accounting_period = current_accounting_period
        self.user_role_name = user_role_name
        self.permissions = permissions
        self.feature_flags = feature_flags
        self.upgrade_version_v3 = upgrade_version_v3
        self.upgrade_version_v7 = upgrade_version_v7
        self.sku = sku
        self.environment = environment
        self.build_date = build_date
