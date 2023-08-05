# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BulkBaselineProcessorRequest(Model):
    """BulkBaselineProcessorRequest.

    :param ignore_weather_adjustments: Defaults to "false". Determines if
     weather adjustments are applied to the reprocessed baseline or not
    :type ignore_weather_adjustments: bool
    :param filters: Filter criteria which determine the meters whose cost
     avoidance baselines will be reprocessed
    :type filters: list[~energycap.sdk.models.FilterEdit]
    """

    _attribute_map = {
        'ignore_weather_adjustments': {'key': 'ignoreWeatherAdjustments', 'type': 'bool'},
        'filters': {'key': 'filters', 'type': '[FilterEdit]'},
    }

    def __init__(self, ignore_weather_adjustments=None, filters=None):
        super(BulkBaselineProcessorRequest, self).__init__()
        self.ignore_weather_adjustments = ignore_weather_adjustments
        self.filters = filters
