# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class FloorAreaSplit(Model):
    """FloorAreaSplit.

    :param destination_account_id: Destination account ID
     There must be an existing relationship between the DestinationAccountId
     and DestinationMeterId <span class='property-internal'>Required</span>
     <span class='property-internal'>Topmost (CostCenter)</span>
    :type destination_account_id: int
    :param destination_meter_id: Destination meter ID
     There must be an existing relationship between the DestinationAccountId
     and DestinationMeterId <span class='property-internal'>Required</span>
     <span class='property-internal'>Topmost (LogicalDevice)</span>
    :type destination_meter_id: int
    :param weighting_factor: Weighting factor to apply in floor area bill
     split for this account and meter <span class='property-info'>Max precision
     of 8</span> <span class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and
     7.92281625142643E+28</span>
    :type weighting_factor: float
    """

    _validation = {
        'destination_account_id': {'required': True},
        'destination_meter_id': {'required': True},
        'weighting_factor': {'required': True, 'minimum': 0},
    }

    _attribute_map = {
        'destination_account_id': {'key': 'destinationAccountId', 'type': 'int'},
        'destination_meter_id': {'key': 'destinationMeterId', 'type': 'int'},
        'weighting_factor': {'key': 'weightingFactor', 'type': 'float'},
    }

    def __init__(self, destination_account_id, destination_meter_id, weighting_factor):
        super(FloorAreaSplit, self).__init__()
        self.destination_account_id = destination_account_id
        self.destination_meter_id = destination_meter_id
        self.weighting_factor = weighting_factor
