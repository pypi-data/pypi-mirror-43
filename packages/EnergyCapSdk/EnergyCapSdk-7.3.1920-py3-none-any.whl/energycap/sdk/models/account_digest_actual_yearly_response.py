# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AccountDigestActualYearlyResponse(Model):
    """AccountDigestActualYearlyResponse.

    :param account_code: The account code
    :type account_code: str
    :param account_info: The account info
    :type account_info: str
    :param account_id: The account identifier
    :type account_id: int
    :param global_use_unit: The use unit of measure
    :type global_use_unit: ~energycap.sdk.models.UnitChild
    :param cost_unit: The cost unit of measure
    :type cost_unit: ~energycap.sdk.models.UnitChild
    :param updated: The date and time the data was updated
    :type updated: datetime
    :param results: An array of yearly data
    :type results:
     list[~energycap.sdk.models.AccountDigestActualYearlyResponseResults]
    :param commodities: An array of yearly data per commodity
    :type commodities:
     list[~energycap.sdk.models.AccountDigestActualYearlyResponseCommodityData]
    """

    _attribute_map = {
        'account_code': {'key': 'accountCode', 'type': 'str'},
        'account_info': {'key': 'accountInfo', 'type': 'str'},
        'account_id': {'key': 'accountId', 'type': 'int'},
        'global_use_unit': {'key': 'globalUseUnit', 'type': 'UnitChild'},
        'cost_unit': {'key': 'costUnit', 'type': 'UnitChild'},
        'updated': {'key': 'updated', 'type': 'iso-8601'},
        'results': {'key': 'results', 'type': '[AccountDigestActualYearlyResponseResults]'},
        'commodities': {'key': 'commodities', 'type': '[AccountDigestActualYearlyResponseCommodityData]'},
    }

    def __init__(self, account_code=None, account_info=None, account_id=None, global_use_unit=None, cost_unit=None, updated=None, results=None, commodities=None):
        super(AccountDigestActualYearlyResponse, self).__init__()
        self.account_code = account_code
        self.account_info = account_info
        self.account_id = account_id
        self.global_use_unit = global_use_unit
        self.cost_unit = cost_unit
        self.updated = updated
        self.results = results
        self.commodities = commodities
